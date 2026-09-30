#!/usr/bin/env python3
"""Publish the allowlisted Reformation course; --check never writes."""
from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_PARTS = {"staff", "facilitator", "reference", "reviews", "review", "history", "evidence", "tests", "work", "__pycache__", ".git", "graded", "answer-keys", "answers"}
SAFE_TAGS = set("a p h1 h2 h3 h4 h5 h6 ul ol li em strong code pre blockquote table caption thead tbody tr th td details summary img hr br div span dl dt dd sup sub del input".split())
VOID_TAGS = {"img", "hr", "br", "input", "meta", "link"}
COMMAND_LANGUAGES = {"bash", "sh", "zsh", "powershell"}
CSS = """*{box-sizing:border-box}html{scroll-behavior:auto}body{font:18px/1.6 system-ui,-apple-system,sans-serif;color:#20221f;background:#fffdf8;margin:0}main,body>nav,footer{max-width:76ch;margin:auto;padding:1rem 1.5rem}h1,h2,h3{line-height:1.25;overflow-wrap:anywhere}h1{font-size:2rem}h2{margin-top:2.2rem}a{color:#174f85;text-underline-offset:.17em}a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid #8c4200;outline-offset:4px}.skip{position:absolute;left:1rem;top:-8rem;background:#fff;padding:.7rem;z-index:5}.skip:focus{top:1rem}pre{background:#f1eee5;border:1px solid #b8b1a1;padding:1rem;overflow:auto;white-space:pre;max-width:100%;font-size:.88rem;line-height:1.5}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere}pre code{overflow-wrap:normal}p code,li code,td code{background:#f1eee5;padding:.1em .2em}.table-scroll{max-width:100%;overflow:auto}table{border-collapse:collapse;min-width:100%;font-size:.94rem}caption{text-align:left;font-weight:600;padding:.5rem 0}th,td{border:1px solid #aaa493;padding:.5rem;vertical-align:top;text-align:left}img{max-width:100%;height:auto}details{border-left:3px solid #a98a51;padding:.4rem 1rem;margin:1rem 0}summary{cursor:pointer;font-weight:600}button{font:inherit;background:#fff;border:1px solid #555;border-radius:3px;padding:.4rem .8rem;cursor:pointer}.copy-status{min-height:1.6em}blockquote{margin:1rem 0;padding:.2rem 1rem;border-left:4px solid #a98a51}nav{display:flex;gap:1rem;flex-wrap:wrap}footer{border-top:1px solid #aaa493;font-size:.9rem}@media(max-width:480px){main,body>nav,footer{padding:.8rem 1rem}h1{font-size:1.65rem}}.module-cards{display:flex;flex-direction:column;gap:.4rem}.module-card{display:block;padding:.4rem .6rem;border-left:3px solid #a98a51;color:inherit;text-decoration:none}.module-card strong{display:block}.module-card span{font-size:.94rem}"""
COPY_JS = """document.querySelectorAll('pre[data-command]').forEach(pre=>{const button=document.createElement('button');button.type='button';button.textContent='Copy command';button.addEventListener('click',async()=>{const status=document.getElementById('copy-status');try{if(!navigator.clipboard)throw new Error('Clipboard unavailable');await navigator.clipboard.writeText(pre.querySelector('code').textContent);status.textContent='Command copied.';}catch{status.textContent='Copy failed. Select the command text and copy it manually.';}});pre.before(button);});"""


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list[Node | str] = field(default_factory=list)

    def text(self) -> str:
        return "".join(child.text() if isinstance(child, Node) else child for child in self.children)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def render(self) -> str:
        if not self.tag:
            return "".join(child.render() if isinstance(child, Node) else html.escape(child, quote=False) for child in self.children)
        attrs = "".join(f' {key}="{html.escape(value, quote=True)}"' for key, value in self.attrs.items())
        if self.tag in VOID_TAGS:
            return f"<{self.tag}{attrs}>"
        inner = "".join(child.render() if isinstance(child, Node) else html.escape(child, quote=False) for child in self.children)
        return f"<{self.tag}{attrs}>{inner}</{self.tag}>"


class TreeParser(HTMLParser):
    def __init__(self, safe_fragment: bool = False):
        super().__init__(convert_charrefs=True)
        self.root = Node("")
        self.stack = [self.root]
        self.safe_fragment = safe_fragment

    def handle_starttag(self, tag, attrs):
        if self.safe_fragment and tag not in SAFE_TAGS:
            raise ValueError(f"active or unsupported HTML element: {tag}")
        attributes = dict((key, value or "") for key, value in attrs)
        if len(attributes) != len(attrs):
            raise ValueError("duplicate HTML attribute")
        for key, value in attributes.items():
            if key.lower().startswith("on") or key in {"srcdoc", "formaction", "style"}:
                raise ValueError(f"active HTML attribute: {key}")
            if key in {"href", "src"} and urlsplit(value).scheme.lower() not in {"", "https", "http", "mailto"}:
                raise ValueError(f"unsafe link scheme: {value}")
        node = Node(tag, attributes)
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if len(self.stack) == 1 or self.stack[-1].tag != tag:
            raise ValueError(f"unbalanced HTML closing tag: {tag}")
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def finish(self) -> Node:
        self.close()
        if len(self.stack) != 1:
            raise ValueError(f"unclosed HTML element: {self.stack[-1].tag}")
        return self.root


def parse_html(text: str, safe_fragment=False) -> Node:
    parser = TreeParser(safe_fragment)
    parser.feed(text)
    return parser.finish()


def safe_relative(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value or ":" in value:
        raise ValueError(f"invalid manifest path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"..", "."} for part in value.split("/")):
        raise ValueError(f"escaping manifest path: {value}")
    return path


def source_path(base: Path, rel: str) -> Path:
    path = base / safe_relative(rel)
    if any(part.lower() in BLOCKED_PARTS or part.startswith(".") for part in Path(rel).parts):
        raise ValueError(f"staff or hidden source cannot be published: {rel}")
    if path.name in {"CUSTODY_CONTRACT.md", "spec.json"} or path.name.lower().startswith(("answer-key", "graded-")):
        raise ValueError(f"staff source cannot be published: {rel}")
    current = path
    while current != base:
        if current.is_symlink():
            raise ValueError(f"symlink source cannot be published: {path}")
        current = current.parent
    if not path.is_file():
        raise ValueError(f"missing publication source: {path}")
    return path


def inventory(root: Path) -> tuple[dict, dict[PurePosixPath, Path], dict[Path, PurePosixPath], set[Path]]:
    course = json.loads((root / "course.json").read_text(encoding="utf-8"))
    modules = course.get("modules", [])
    if [module.get("id") for module in modules] != [f"{i:02d}" for i in range(10)]:
        raise ValueError("manifest must enumerate exactly ten modules in order, 00–09")
    if course.get("schema_version") != 1 or course.get("site_dir") != "site" or course.get("course_id") != "AI_Harness_Bootcamp_2":
        raise ValueError("unsupported course manifest identity")
    boot = root / safe_relative(course["source_root"])
    if boot.resolve() != root.resolve() / "AI_Harness_Bootcamp_2" or boot.is_symlink():
        raise ValueError("source_root must be the Reformation module tree")
    destinations: dict[PurePosixPath, Path] = {}
    sources: dict[Path, PurePosixPath] = {}
    pages: set[Path] = set()

    def add(base: Path, src: str, dest: str, page: bool = False):
        source = source_path(base, src)
        target = safe_relative(dest)
        if any(part.lower() in BLOCKED_PARTS for part in target.parts):
            raise ValueError(f"staff destination: {target}")
        if target in destinations:
            raise ValueError(f"duplicate publication destination: {target}")
        if source in sources:
            raise ValueError(f"duplicate publication source: {source}")
        if not page and source.suffix.lower() in {".html", ".htm", ".pyc"}:
            raise ValueError(f"untrusted or generated raw artifact cannot be published: {source}")
        destinations[target] = source
        sources[source] = target
        if page:
            if source.suffix != ".md" or target.suffix != ".html":
                raise ValueError(f"instructional page must map Markdown to HTML: {source}")
            pages.add(source)

    add(boot, course["index"]["source"], course["index"]["dest"], True)
    for module in modules:
        directory = module["directory"]
        safe_relative(directory)
        if not re.fullmatch(rf"module-{module['id']}-[a-z0-9-]+", directory):
            raise ValueError(f"module ID/directory mismatch: {directory}")
        base = boot / directory
        prefix = PurePosixPath(course["course_id"]) / directory
        for page in module["pages"]:
            add(base, page["source"], str(prefix / page["dest"]), True)
        for kind in ("figures", "scripts"):
            for entry in module.get(kind, []):
                add(base, entry["source"], str(prefix / entry["dest"]))
        for relative in module.get("raw_downloads", []):
            add(base, relative, str(prefix / relative))
        for relative in module.get("download_dirs", []):
            folder = base / safe_relative(relative)
            if not folder.is_dir() or folder.is_symlink():
                raise ValueError(f"missing or linked exercise directory: {folder}")
            for source in sorted(folder.rglob("*")):
                if source.is_symlink():
                    raise ValueError(f"linked exercise source: {source}")
                if source.is_file():
                    rel = source.relative_to(base).as_posix()
                    if any(part == "__pycache__" for part in source.parts) or source.suffix == ".pyc":
                        continue
                    add(base, rel, str(prefix / rel))
        verifier = module.get("verifier_download")
        if verifier and (base / verifier) not in sources:
            add(base, verifier, str(prefix / verifier))
    for entry in course.get("shared_downloads", []):
        add(root, entry["source"], entry["dest"])
    return course, destinations, sources, pages


def rewrite_link(value: str, source: Path, dest: PurePosixPath, mapping: dict[Path, PurePosixPath], course: dict, root: Path) -> str:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return value
    if parsed.path.startswith("/"):
        raise ValueError(f"source link must be relative: {source}: {value}")
    target = Path(os.path.normpath(source.parent / unquote(parsed.path)))
    if target not in mapping:
        raise ValueError(f"unlisted local link: {source.relative_to(root)} -> {value}")
    path = posixpath.relpath(str(mapping[target]), str(dest.parent))
    return urlunsplit(("", "", quote(path, safe="/-._~"), parsed.query, parsed.fragment))


def procedure_errors(tree: Node, label: str) -> list[str]:
    errors = []
    nodes = list(tree.walk())
    if sum(node.tag == "h1" for node in nodes) != 1:
        errors.append(f"{label}: expected one h1")
    blocks = [node for node in nodes if node.tag in {"h1", "h2", "h3", "h4", "p", "pre", "summary"}]
    for index, node in enumerate(blocks):
        if node.tag != "pre":
            continue
        codes = [child for child in node.children if isinstance(child, Node) and child.tag == "code"]
        language = codes[0].attrs.get("class", "").removeprefix("language-") if len(codes) == 1 else ""
        if not language or not codes[0].attrs.get("class", "").startswith("language-"):
            errors.append(f"{label}: every fenced block needs an explicit language")
            continue
        if language not in COMMAND_LANGUAGES:
            continue
        previous = index - 1
        while previous >= 0 and blocks[previous].tag not in {"h1", "h2", "h3", "h4", "pre"}:
            previous -= 1
        before = " ".join(block.text() for block in blocks[previous + 1:index])
        end = index + 1
        while end < len(blocks) and blocks[end].tag not in {"h1", "h2", "h3", "h4"}:
            end += 1
        after = " ".join(block.text() for block in blocks[index + 1:end] if block.tag != "pre")
        if not re.search(r"\bTerminal\s*:", before, re.I) or not re.search(r"\b(user|administrator|admin|root|elevat\w*|privilege)\b", before, re.I):
            errors.append(f"{label}: {language} command lacks its terminal/privilege label")
        if not re.search(r"\b(Expected|Expect|You should see|You.ll see|Observation)\b", after, re.I):
            errors.append(f"{label}: {language} command lacks an associated expected observation")
        if not re.search(r"\b(Stop|HOLD)\b", after, re.I):
            errors.append(f"{label}: {language} command lacks an associated stop condition")
        if not re.search(r"\b(Recover\w*|Retry|Rerun|Restore|Ask|Choose|Correct|Return|Contact)\b", after, re.I):
            errors.append(f"{label}: {language} command lacks an associated recovery")
        if re.search(r"^(?:PASS|HOLD|FAIL|READY|TOOL PROOF PASS)(?::|$)", codes[0].text(), re.M):
            errors.append(f"{label}: observed output must be separate from command text")
        node.attrs["data-command"] = language
    return errors


def render_page(source: Path, dest: PurePosixPath, mapping: dict[Path, PurePosixPath], course: dict, root: Path) -> bytes:
    fragment = markdown.markdown(source.read_text(encoding="utf-8"), extensions=["fenced_code", "tables", "toc", "md_in_html"], extension_configs={"tables": {"use_align_attribute": True}}, output_format="html")
    try:
        tree = parse_html(fragment, True)
    except ValueError as error:
        raise ValueError(f"{source.relative_to(root)}: {error}") from error
    errors = procedure_errors(tree, source.relative_to(root).as_posix())
    if errors:
        raise ValueError("\n".join(errors))
    heading = "Course data"
    title = next(node.text() for node in tree.walk() if node.tag == "h1")
    for node in list(tree.walk()):
        if node.tag.startswith("h") and node.tag[1:].isdigit():
            heading = node.text()
        if node.tag == "table":
            node.children.insert(0, Node("caption", {}, [heading]))
        if node.tag == "th":
            node.attrs["scope"] = "col"
        if node.tag == "img" and not node.attrs.get("alt", "").strip():
            raise ValueError(f"{source}: image needs alternative text")
        for attr in ("href", "src"):
            if attr in node.attrs:
                node.attrs[attr] = rewrite_link(node.attrs[attr], source, dest, mapping, course, root)
    def wrap_tables(parent: Node):
        for i, child in enumerate(parent.children):
            if isinstance(child, Node):
                wrap_tables(child)
                if child.tag == "table":
                    parent.children[i] = Node("div", {"class": "table-scroll", "tabindex": "0", "role": "region", "aria-label": child.children[0].text()}, [child])
    wrap_tables(tree)
    index_href = posixpath.relpath("index.html", str(dest.parent))
    module_match = re.search(r"module-(\d{2})-", source.as_posix())
    navigation = f'<a href="{index_href}">All assignments</a>'
    if module_match:
        module = course["modules"][int(module_match.group(1))]
        module_dest = PurePosixPath(course["course_id"]) / module["directory"] / "README.html"
        navigation += f'<a href="{posixpath.relpath(str(module_dest), str(dest.parent))}">Assignment overview</a>'
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><a class="skip" href="#main">Skip to content</a><nav aria-label="Course">{navigation}</nav><main id="main">{tree.render()}<p id="copy-status" class="copy-status" role="status" aria-live="polite"></p></main><footer>Fictional, class-only work. A passing check does not authorize a real movement.</footer><script>{COPY_JS}</script></body></html>
'''
    return document.encode("utf-8")


def validate_links(outputs: dict[PurePosixPath, bytes]) -> None:
    parsed = {path: parse_html(data.decode("utf-8")) for path, data in outputs.items() if path.suffix == ".html"}
    anchors = {}
    for path, tree in parsed.items():
        ids = [node.attrs["id"] for node in tree.walk() if "id" in node.attrs]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate HTML anchor: {path}")
        anchors[path] = set(ids)
    for path, tree in parsed.items():
        for node in tree.walk():
            for attr in ("href", "src"):
                value = node.attrs.get(attr)
                if value is None:
                    continue
                url = urlsplit(value)
                if url.scheme or url.netloc:
                    continue
                target = PurePosixPath(posixpath.normpath(str(path.parent / unquote(url.path)))) if url.path else path
                if target not in outputs:
                    raise ValueError(f"broken published link: {path} -> {value}")
                if url.fragment and target in anchors and unquote(url.fragment) not in anchors[target]:
                    raise ValueError(f"missing published anchor: {path} -> {value}")


def build(root: Path = ROOT, check: bool = False) -> int:
    course, destinations, mapping, pages = inventory(root)
    outputs = {dest: render_page(source, dest, mapping, course, root) if source in pages else source.read_bytes() for dest, source in destinations.items()}
    validate_links(outputs)
    site = root / "site"
    if site.is_symlink():
        raise ValueError("site must not be a symlink")
    existing = set()
    if site.exists():
        for path in site.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"linked public output: {path}")
            if path.is_file():
                existing.add(PurePosixPath(path.relative_to(site).as_posix()))
    extras = existing - outputs.keys()
    if extras:
        raise ValueError("unlisted public output (preserved): " + ", ".join(map(str, sorted(extras))))
    if check:
        mismatches = [str(dest) for dest, data in outputs.items() if dest not in existing or (site / dest).read_bytes() != data]
        if mismatches:
            raise ValueError("missing or stale published bytes: " + ", ".join(mismatches))
        # Read the actual published documents, not only regenerated fragments.
        validate_links({dest: (site / dest).read_bytes() for dest in outputs})
    else:
        for dest, data in outputs.items():
            target = site / dest
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(f"PASS: {len(pages)} pages and {len(outputs) - len(pages)} downloads {'checked byte-for-byte' if check else 'published'}; public links and procedure structure checked")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        return build(check=args.check)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"HOLD: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
