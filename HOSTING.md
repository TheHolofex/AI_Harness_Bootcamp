# Hosting the course site (Railway)

Password-gated static host for the bootcamp website. Learners open `/site/` after entering one shared password from an environment variable.

## Course surface

The repository root is the deployment working directory. The password-gated server sends learners to the canonical website:

```bash
python server.py
# → http://localhost:8080/site/
```

The learner navigation stays inside `site/`. Raw exercise files under `operator/`, `mission_flesh/`, and `instruments/` are working inputs in the cloned course repository, not an alternate web course.

## Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `SITE_PASSWORD` | **Yes** (production) | Single shared cohort site password |
| `PORT` | Set by Railway | Listen port |
| `SITE_SECRET` | Optional | Cookie HMAC secret; defaults to a key derived from `SITE_PASSWORD` |
| `COOKIE_MAX_AGE` | Optional | Session length in seconds (default 14 days) |
| `ALLOW_OPEN` | Local only | `1` allows start with empty `SITE_PASSWORD` — **never** on Railway |

## Local

Preferred: put the password in a gitignored `.env` (see `.env.example`). `server.py` loads it automatically and will not override real environment variables.

```bash
cd /path/to/AI_Harness_Bootcamp
cp .env.example .env   # then edit SITE_PASSWORD=
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python server.py
# open http://127.0.0.1:8080/site/
```

Or export once in the shell:

```bash
export SITE_PASSWORD='choose-a-cohort-password'
python server.py
```

Ungated local (dev only):

```bash
ALLOW_OPEN=1 python server.py
```

## Railway

1. New project → Deploy from this GitHub repo (root directory = repo root).
2. Service variables:
   - `SITE_PASSWORD` = the cohort password (mark sensitive).
   - Optional: `SITE_SECRET` = long random string (rotate independently of the password).
3. Generate a domain on the service.
4. Health check path is `/healthz` (no auth; returns `ok`).
5. Open `https://<your-domain>/` → login → redirects to `/site/`.

`railway.toml`, `Procfile`, and `nixpacks.toml` start `python server.py`. No extra dependencies.

## Cohort repository visibility

Learners clone the exercise files without GitHub accounts during B0, so the repository must be public for the bootcamp window. The password gate still protects the hosted course navigation; repository visibility is a separate control.

Before the install clinic, verify the setting and make the repository public if needed:

```bash
gh repo view TheHolofex/AI_Harness_Bootcamp --json visibility --jq .visibility
gh repo edit TheHolofex/AI_Harness_Bootcamp \
  --visibility public \
  --accept-visibility-change-consequences
```

After the bootcamp, make it private again and verify the result:

```bash
gh repo edit TheHolofex/AI_Harness_Bootcamp \
  --visibility private \
  --accept-visibility-change-consequences
gh repo view TheHolofex/AI_Harness_Bootcamp --json visibility --jq .visibility
```

Changing visibility affects every anonymous clone and existing fork relationship. Run the private command only after the final learner download window has closed.

### Rotate password

Change `SITE_PASSWORD` in Railway and redeploy (or restart). Existing cookies stop working immediately because the token is tied to the password (and `SITE_SECRET` if set).

## What the gate is (and is not)

- **Is:** a shared classroom door so the URL is not a public index of courseware.
- **Is not:** per-student accounts, audit logging, or strong DRM.
- Staff-only files are **not** served over HTTP even after login (answer keys, pin sheet, `FACILITATOR_KEY.md`, `.git`, `.github`, `*.py`, env files). Keep filled pins and secrets out of git.

## Endpoints

| Path | Auth | Role |
|---|---|---|
| `/healthz` | No | Liveness |
| `/__login` | No | Password form |
| `/__logout` | Cookie clear | End session |
| `/` | Yes | Redirect → `/site/` |
| `/site/…` | Yes | Canonical course website |
| Unlinked repo files | Yes, unless blocked | Local exercise inputs; not course navigation |

## Smoke test

```bash
export SITE_PASSWORD='test-pass'
python server.py &
sleep 1
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/healthz
# 200
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/site/
# 303 → login
curl -sS -c /tmp/ahb.ck -b /tmp/ahb.ck -X POST \
  -d 'password=test-pass&next=/site/' \
  -o /dev/null -w '%{http_code}\n' \
  http://127.0.0.1:8080/__login
# 303 with Set-Cookie
curl -sS -b /tmp/ahb.ck -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/site/
# 200
curl -sS -b /tmp/ahb.ck -o /dev/null -w '%{http_code}\n' \
  http://127.0.0.1:8080/lead/MANY_MINDS_ANSWER_KEY.md
# 404 (staff-only)
```
