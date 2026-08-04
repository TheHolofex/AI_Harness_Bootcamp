#!/usr/bin/env python3
"""Password-gated static host for the AI Harness Bootcamp.

Serves the repository root and routes learners to the canonical website at
`/site/`. Raw exercise files remain available to cloned workspaces, but the
website does not use them as an alternate reading path.

    python3 -m http.server 8080
    → http://localhost:8080/site/

Environment
-----------
SITE_PASSWORD   Required in production. Shared cohort site password.
STAFF_PASSWORD  Optional, and separate from SITE_PASSWORD. Unlocks staff/
                (answer keys, facilitator keys, cohort pin sheet). Leave it
                unset and staff/ is unreachable over HTTP by anyone.
PORT            Listen port (Railway sets this). Default 8080.
BIND_HOST       Default 0.0.0.0
SITE_SECRET     Optional cookie-signing secret. Defaults to a key derived
                from SITE_PASSWORD (fine for a single shared password).
COOKIE_NAME     Default ahb_site_auth
STAFF_COOKIE_NAME  Default ahb_staff_auth
COOKIE_MAX_AGE  Seconds. Default 1209600 (14 days).
ALLOW_OPEN      If "1" and SITE_PASSWORD is empty, serve without a gate
                (local only). Never set this on Railway.

Two audiences, two credentials
------------------------------
SITE_PASSWORD is handed to the whole cohort, so holding it proves nothing
about who you are — a cohort login must never reach an answer key. Staff
material therefore sits behind its own password on its own cookie:

  * No cookie at all      → login page. Nothing under staff/ is served,
                            and nothing else is either.
  * Cohort cookie only    → the course site. staff/ returns 404, exactly as
                            it does for a logged-out stranger.
  * Staff cookie          → the course site plus staff/.

ALLOW_OPEN does not grant staff access; only STAFF_PASSWORD does.

Always blocked (even for staff): .git, .env*, secrets/, venvs, .github/,
*.py, authoring/build sources, analysis notes, and — outside staff/ — the
STAFF_ONLY_PATHS list and any *FACILITATOR_KEY.md / *ANSWER_KEY.md file.
"""

from __future__ import annotations

import hashlib
import hmac
import http.cookies
import mimetypes
import os
import sys
import urllib.parse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from a local .env if present.

    Does not override variables already set in the process environment
    (Railway / shell win). No external dependency.
    """
    env_path = path or (REPO_ROOT / ".env")
    if not env_path.is_file():
        return
    try:
        text = env_path.read_text(encoding="utf-8")
    except OSError:
        return
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


load_dotenv()

COOKIE_NAME = os.environ.get("COOKIE_NAME", "ahb_site_auth")
STAFF_COOKIE_NAME = os.environ.get("STAFF_COOKIE_NAME", "ahb_staff_auth")
COOKIE_MAX_AGE = int(os.environ.get("COOKIE_MAX_AGE", str(14 * 24 * 3600)))
BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")

# The one directory a staff login opens. Not in the git tree at all — staff
# receive it out of band and drop it at the repo root (see staff/README.md).
STAFF_ROOT = "staff"

BLOCKED_PREFIXES = (
    ".git/",
    ".git",
    "secrets/",
    "venv/",
    ".venv/",
    "__pycache__/",
    ".github/",
    "node_modules/",
    "scripts/",
    "resources/handouts/",
    "resources/figures/",
)

# Cohort password is shared with students — keep answer keys off HTTP.
# operator/CAPABILITIES.md is deliberately NOT here because it is a working
# exercise file used throughout the course.
#
# The key files now live under staff/ and are reachable only with a staff
# login. Their former locations stay on this list so that a stray copy dropped
# back into the course tree — a facilitator's convenience checkout, a bad
# merge — is still refused over HTTP.
STAFF_ONLY_PATHS = {
    "lead/MANY_MINDS_ANSWER_KEY.md",
    "lead/COHORT_PIN.md",
    "instruments/p2_test_suite/engineering/FACILITATOR_KEY.md",
    "instruments/p2_test_suite/mission_ops/FACILITATOR_KEY.md",
    "instruments/endpoint_case_suite/engineering/FACILITATOR_KEY.md",
    "instruments/endpoint_case_suite/mission_ops/FACILITATOR_KEY.md",
    "instruments/p3_frozen_brief/engineering/FACILITATOR_KEY.md",
    "instruments/p3_frozen_brief/mission_ops/FACILITATOR_KEY.md",
    "instruments/p8_hold_degrade/FACILITATOR_KEY.md",
    "mission_flesh/p5/FACILITATOR_KEY.md",
    "resources/AUTHORING.md",
    "resources/catalog.json",
    "resources/scopes.json",
}

BLOCKED_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "server.py",
    "railway.toml",
    "Procfile",
    "nixpacks.toml",
}


def env_password() -> str:
    return os.environ.get("SITE_PASSWORD", "")


def env_staff_password() -> str:
    return os.environ.get("STAFF_PASSWORD", "").strip()


def allow_open() -> bool:
    return os.environ.get("ALLOW_OPEN", "").strip().lower() in {"1", "true", "yes"}


def signing_key(password: str) -> bytes:
    secret = os.environ.get("SITE_SECRET", "").strip()
    if secret:
        return secret.encode("utf-8")
    return hashlib.sha256(f"ahb-site-v1:{password}".encode("utf-8")).digest()


def auth_token(password: str) -> str:
    return hmac.new(signing_key(password), b"authenticated", hashlib.sha256).hexdigest()


def token_valid(password: str, token: str | None) -> bool:
    if not password or not token:
        return False
    return hmac.compare_digest(auth_token(password), token)


def staff_signing_key(staff_password: str) -> bytes:
    """Key for the staff cookie.

    Always bound to STAFF_PASSWORD, even when SITE_SECRET is set, so that
    rotating the staff password invalidates every outstanding staff cookie
    and knowing the cohort password never yields the staff token.
    """
    secret = os.environ.get("SITE_SECRET", "").strip() or "ahb-staff-v1"
    return hashlib.sha256(f"{secret}:staff:{staff_password}".encode("utf-8")).digest()


def staff_auth_token(staff_password: str) -> str:
    return hmac.new(
        staff_signing_key(staff_password), b"staff-authenticated", hashlib.sha256
    ).hexdigest()


def staff_token_valid(staff_password: str, token: str | None) -> bool:
    if not staff_password or not token:
        return False
    return hmac.compare_digest(staff_auth_token(staff_password), token)


def normalize_rel(rel_path: str) -> str:
    return rel_path.replace("\\", "/").lstrip("/")


def in_staff_root(rel_path: str) -> bool:
    norm = normalize_rel(rel_path)
    return norm == STAFF_ROOT or norm.startswith(STAFF_ROOT + "/")


def is_blocked(rel_path: str, staff: bool = False) -> bool:
    """Should this repo-relative path be refused?

    ``staff`` says the request carried a valid staff cookie. It opens exactly
    one door — the staff/ directory — and nothing else. It defaults to False so
    that any caller which forgets to pass it fails closed.
    """
    norm = normalize_rel(rel_path)
    if not norm or norm == ".":
        return False
    name = Path(norm).name
    lowered = norm.lower()

    # Refused for everyone, staff included: source, secrets, build inputs.
    if name in BLOCKED_NAMES or name.startswith(".env"):
        return True
    if name.endswith(".py"):
        return True
    for prefix in BLOCKED_PREFIXES:
        if lowered == prefix.rstrip("/") or lowered.startswith(prefix):
            return True

    # staff/ is the one place a staff login reaches. For everyone else it is a
    # 404, indistinguishable from a path that does not exist.
    if in_staff_root(norm):
        return not staff

    # Outside staff/, the key rules stand for staff and students alike: a key
    # file has no business in the course tree, whoever is asking.
    if norm in STAFF_ONLY_PATHS:
        return True
    if name.endswith("FACILITATOR_KEY.md") or name.endswith("ANSWER_KEY.md"):
        return True
    return False


def safe_next_path(raw: str | None, default: str = "/site/") -> str:
    if not raw:
        return default
    path = urllib.parse.unquote(raw)
    if not path.startswith("/") or path.startswith("//") or "\\" in path:
        return default
    if any(part == ".." for part in path.split("/")):
        return default
    return path


LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Harness Bootcamp · Sign in</title>
  <style>
    :root {{
      --ink: #1a1a1a;
      --muted: #5a5a5a;
      --line: #d8d4cc;
      --paper: #f7f4ee;
      --red: #b91c1c;
      --field: #fff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
      background: var(--paper);
      color: var(--ink);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}
    .card {{
      width: 100%;
      max-width: 26rem;
      background: var(--field);
      border: 1px solid var(--line);
      padding: 2rem 1.75rem 1.75rem;
      box-shadow: 0 1px 0 rgba(0,0,0,.04);
    }}
    .mark {{
      width: 0.7rem; height: 0.7rem; border-radius: 50%;
      background: var(--red); display: inline-block; margin-right: 0.5rem;
      vertical-align: middle;
    }}
    .brand {{
      font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase;
      color: var(--muted); margin: 0 0 1.25rem;
    }}
    h1 {{
      font-size: 1.35rem; font-weight: 600; margin: 0 0 0.5rem; line-height: 1.25;
    }}
    p {{ margin: 0 0 1.25rem; color: var(--muted); font-size: 0.95rem; line-height: 1.45; }}
    label {{
      display: block; font-size: 0.8rem; letter-spacing: 0.04em;
      text-transform: uppercase; color: var(--muted); margin-bottom: 0.4rem;
    }}
    input[type=password] {{
      width: 100%; padding: 0.7rem 0.75rem; border: 1px solid var(--line);
      font-size: 1rem; background: #fff; color: var(--ink);
    }}
    input[type=password]:focus {{ outline: 2px solid #1a1a1a; outline-offset: 1px; }}
    button {{
      margin-top: 1rem; width: 100%; padding: 0.75rem 1rem;
      border: 0; background: var(--ink); color: #fff; font-size: 0.95rem;
      letter-spacing: 0.03em; cursor: pointer;
    }}
    button:hover {{ background: #000; }}
    .err {{
      background: #fef2f2; border: 1px solid #fecaca; color: #991b1b;
      padding: 0.6rem 0.75rem; margin-bottom: 1rem; font-size: 0.9rem;
    }}
    .foot {{ margin-top: 1.25rem; font-size: 0.8rem; color: var(--muted); }}
  </style>
</head>
<body>
  <div class="card">
    <p class="brand"><span class="mark" aria-hidden="true"></span>Starzl Enterprises</p>
    <h1>AI Harness Bootcamp</h1>
    <p>This course site is shared with the cohort. Enter the site password staff gave you.</p>
    {error}
    <form method="post" action="/__login">
      <input type="hidden" name="next" value="{next}" />
      <label for="password">Site password</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required autofocus />
      <button type="submit">Enter course site</button>
    </form>
    <p class="foot">Session lasts about two weeks on this browser. Do not post the password in chat logs or screenshots. Staff: enter the staff password here instead — it opens the same site plus your own material.</p>
  </div>
</body>
</html>
"""


class BootcampHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **getattr(SimpleHTTPRequestHandler, "extensions_map", {}),
        # text/plain, not text/markdown: browsers download an unknown type but
        # render text/plain inline, and block pages link straight to .md files.
        ".md": "text/plain; charset=utf-8",
        ".markdown": "text/plain; charset=utf-8",
        ".yaml": "text/yaml; charset=utf-8",
        ".yml": "text/yaml; charset=utf-8",
        ".toml": "text/plain; charset=utf-8",
        ".svg": "image/svg+xml",
        ".json": "application/json",
        ".wasm": "application/wasm",
        ".html": "text/html",
        ".css": "text/css",
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".ico": "image/x-icon",
        ".txt": "text/plain",
        ".csv": "text/csv",
    }

    def __init__(
        self,
        *args,
        password: str,
        open_mode: bool,
        staff_password: str = "",
        **kwargs,
    ):
        self.password = password
        self.open_mode = open_mode
        self.staff_password = staff_password
        super().__init__(*args, **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(
        self,
        code: int,
        body: bytes,
        content_type: str,
        headers: list[tuple[str, str]] | None = None,
    ) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        no_store = code >= 400 or content_type.startswith("text/html")
        self.send_header(
            "Cache-Control",
            "no-store" if no_store else "public, max-age=300",
        )
        if headers:
            for k, v in headers:
                self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _read_cookie(self, cookie_name: str) -> str | None:
        raw = self.headers.get("Cookie")
        if not raw:
            return None
        jar = http.cookies.SimpleCookie()
        try:
            jar.load(raw)
        except http.cookies.CookieError:
            return None
        morsel = jar.get(cookie_name)
        return morsel.value if morsel else None

    def _read_cookie_token(self) -> str | None:
        return self._read_cookie(COOKIE_NAME)

    def _staff_authorized(self) -> bool:
        """True only for a valid staff cookie.

        Deliberately independent of open_mode and of the cohort password: an
        ungated local run still refuses staff/ unless STAFF_PASSWORD is set and
        the staff login has actually happened.
        """
        if not self.staff_password:
            return False
        return staff_token_valid(
            self.staff_password, self._read_cookie(STAFF_COOKIE_NAME)
        )

    def _authorized(self) -> bool:
        if self.open_mode:
            return True
        if self._staff_authorized():
            return True
        if not self.password:
            return False
        return token_valid(self.password, self._read_cookie_token())

    def _login_html(self, next_path: str, bad: bool = False) -> bytes:
        err = (
            '<div class="err">That password did not match. '
            "Try again, or ask staff for the cohort site password.</div>"
            if bad
            else ""
        )
        safe = safe_next_path(next_path).replace('"', "&quot;")
        return LOGIN_PAGE.format(error=err, next=safe).encode("utf-8")

    def _cookie_header(self, cookie_name: str, token: str) -> str:
        proto = self.headers.get("X-Forwarded-Proto", "").split(",")[0].strip().lower()
        secure = "; Secure" if proto == "https" else ""
        return (
            f"{cookie_name}={token}; Path=/; HttpOnly; SameSite=Lax; "
            f"Max-Age={COOKIE_MAX_AGE}{secure}"
        )

    def _set_auth_cookie_header(self) -> str:
        return self._cookie_header(COOKIE_NAME, auth_token(self.password))

    def _set_staff_cookie_header(self) -> str:
        return self._cookie_header(
            STAFF_COOKIE_NAME, staff_auth_token(self.staff_password)
        )

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.rstrip("/") != "/__login":
            self._send(404, b"Not found\n", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            self._send(400, b"Bad request\n", "text/plain; charset=utf-8")
            return
        if length < 0 or length > 4096:
            self._send(400, b"Bad request\n", "text/plain; charset=utf-8")
            return
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = urllib.parse.parse_qs(raw, keep_blank_values=True)
        submitted = (form.get("password") or [""])[0]
        next_path = safe_next_path((form.get("next") or ["/site/"])[0])

        # One field, two passwords. Staff is checked first: a staff member gets
        # the staff cookie *and* the ordinary site cookie, so one sign-in serves
        # the whole site. Students match only the cohort password and get one.
        cookies: list[str] = []
        if self.staff_password and hmac.compare_digest(submitted, self.staff_password):
            cookies.append(self._set_staff_cookie_header())
            if self.password:
                cookies.append(self._set_auth_cookie_header())
        elif self.password and hmac.compare_digest(submitted, self.password):
            cookies.append(self._set_auth_cookie_header())

        if cookies:
            self.send_response(303)
            self.send_header("Location", next_path)
            for cookie in cookies:
                self.send_header("Set-Cookie", cookie)
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        self._send(401, self._login_html(next_path, bad=True), "text/html; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        self._handle_read()

    def do_HEAD(self) -> None:  # noqa: N802
        self._handle_read()

    def _handle_read(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)

        if path in {"/healthz", "/health"}:
            self._send(
                200,
                b"ok\n",
                "text/plain; charset=utf-8",
                [("Cache-Control", "no-store")],
            )
            return

        if path.rstrip("/") == "/__login":
            next_q = safe_next_path(
                (urllib.parse.parse_qs(parsed.query).get("next") or ["/site/"])[0]
            )
            self._send(200, self._login_html(next_q), "text/html; charset=utf-8")
            return

        if path.rstrip("/") == "/__logout":
            self.send_response(303)
            self.send_header("Location", "/__login")
            for cookie_name in (COOKIE_NAME, STAFF_COOKIE_NAME):
                self.send_header(
                    "Set-Cookie",
                    f"{cookie_name}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0",
                )
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return

        if not self._authorized():
            accept = self.headers.get("Accept", "")
            next_path = path if path.startswith("/") else "/site/"
            if "text/html" in accept or accept == "" or "*/*" in accept:
                loc = "/__login?next=" + urllib.parse.quote(next_path, safe="/")
                self.send_response(303)
                self.send_header("Location", loc)
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", "0")
                self.end_headers()
            else:
                self._send(401, b"Unauthorized\n", "text/plain; charset=utf-8")
            return

        if path in {"", "/"}:
            self.send_response(302)
            self.send_header("Location", "/site/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        rel = path.lstrip("/")
        if is_blocked(rel, staff=self._staff_authorized()):
            self._send(404, b"Not found\n", "text/plain; charset=utf-8")
            return

        if self.command == "HEAD":
            super().do_HEAD()
        else:
            super().do_GET()

    def translate_path(self, path: str) -> str:
        root = REPO_ROOT.resolve()
        translated = super().translate_path(path)
        try:
            resolved = Path(translated).resolve()
            rel = str(resolved.relative_to(root)).replace("\\", "/")
        except Exception:
            return str(root / "__blocked__")
        if is_blocked(rel, staff=self._staff_authorized()):
            return str(root / "__blocked__")
        return str(resolved)

    def list_directory(self, path: str):
        self._send(403, b"Directory listing disabled\n", "text/plain; charset=utf-8")
        return None


def main() -> int:
    password = env_password()
    staff_password = env_staff_password()
    open_mode = False
    if not password:
        if allow_open():
            open_mode = True
            print(
                "WARNING: ALLOW_OPEN=1 and SITE_PASSWORD empty — serving without gate",
                file=sys.stderr,
            )
        else:
            print(
                "SITE_PASSWORD is not set. Refusing to start.\n"
                "  export SITE_PASSWORD='your-cohort-password'\n"
                "  # local dev without a gate: ALLOW_OPEN=1",
                file=sys.stderr,
            )
            return 1

    if staff_password and password and staff_password == password:
        print(
            "STAFF_PASSWORD must differ from SITE_PASSWORD — the cohort holds\n"
            "SITE_PASSWORD, so an identical staff password hands every student\n"
            "the answer keys. Refusing to start.",
            file=sys.stderr,
        )
        return 1

    port = int(os.environ.get("PORT", "8080"))
    handler = partial(
        BootcampHandler,
        directory=str(REPO_ROOT),
        password=password,
        open_mode=open_mode,
        staff_password=staff_password,
    )
    mimetypes.add_type("text/plain", ".md")
    mimetypes.add_type("text/yaml", ".yaml")
    mimetypes.add_type("text/yaml", ".yml")

    server = ThreadingHTTPServer((BIND_HOST, port), handler)
    mode = "open" if open_mode else "password-gated"
    staff_dir = (REPO_ROOT / STAFF_ROOT).is_dir()
    if staff_password:
        note = "staff/ served to a staff login" if staff_dir else (
            "STAFF_PASSWORD set but staff/ is not present on this machine"
        )
    else:
        note = "staff/ unreachable (STAFF_PASSWORD unset)"
    print(
        f"AI Harness Bootcamp host ({mode}) on http://{BIND_HOST}:{port}/site/\n"
        f"  {note}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutdown", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
