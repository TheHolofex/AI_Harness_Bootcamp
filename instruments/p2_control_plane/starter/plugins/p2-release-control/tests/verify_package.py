#!/usr/bin/env python3
"""Verify the P2 control-plane package and release-gate wiring."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.9 and 3.10 use the strict local fallback below.
    tomllib = None  # type: ignore[assignment]


PLUGIN = Path(__file__).resolve().parents[1]
STARTER = PLUGIN.parents[1]
MARKETPLACE = STARTER / ".agents/plugins/marketplace.json"
CONTRACT = STARTER / "P2_CONTROL_PLANE.json"
CODEX_CONFIG = STARTER / ".codex/config.toml"
AGENT_DIRECTORY = STARTER / ".codex/agents"
TERRA_MODEL = "gpt-5.6-terra"
DOCS_MCP_URL = "https://developers.openai.com/mcp"

REQUIRED_EVIDENCE = {
    "inputs/p1/SOURCE_MANIFEST.md",
    "inputs/p1/AUDIT.md",
    "inputs/p1/RELEASE_RECORD.md",
    "out/PLUGIN_REVIEW.md",
    "out/EVIDENCE_MAP.md",
    "out/CONFIG_EVIDENCE.md",
    "out/DECISION_REVIEW.md",
    "out/RUN_RECEIPT.md",
}
REQUIRED_SECRET_PATTERNS = {
    r"sk-[A-Za-z0-9_-]{16,}",
    r"xai-[A-Za-z0-9_-]{16,}",
}


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path} must contain one JSON object"
    return data


def strip_toml_comment(value: str) -> str:
    in_basic = False
    in_literal = False
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\" and in_basic:
            escaped = True
        elif character == '"' and not in_literal:
            in_basic = not in_basic
        elif character == "'" and not in_basic:
            in_literal = not in_literal
        elif character == "#" and not in_basic and not in_literal:
            return value[:index].rstrip()
    return value.rstrip()


def parse_toml_scalar(raw: str, path: Path, line_number: int) -> Any:
    value = strip_toml_comment(raw).strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"[+-]?[0-9]+", value):
        return int(value)
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1]
    raise AssertionError(f"unsupported TOML value at {path}:{line_number}: {value!r}")


def load_toml_fallback(path: Path) -> dict[str, Any]:
    """Parse the strict TOML subset used by this dependency-free starter package."""
    document: dict[str, Any] = {}
    table = document
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line_number = index + 1
        stripped = lines[index].strip()
        index += 1
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("["):
            assert stripped.endswith("]") and not stripped.startswith("[["), (
                f"invalid TOML table at {path}:{line_number}"
            )
            parts = stripped[1:-1].split(".")
            assert all(re.fullmatch(r"[A-Za-z0-9_-]+", part) for part in parts), (
                f"invalid TOML table name at {path}:{line_number}"
            )
            table = document
            for part in parts:
                child = table.setdefault(part, {})
                assert isinstance(child, dict), f"TOML table conflicts with key at {path}:{line_number}"
                table = child
            continue

        assert "=" in stripped, f"invalid TOML assignment at {path}:{line_number}"
        key, raw_value = (part.strip() for part in stripped.split("=", 1))
        assert re.fullmatch(r"[A-Za-z0-9_-]+", key), f"invalid TOML key at {path}:{line_number}"
        assert key not in table, f"duplicate TOML key at {path}:{line_number}: {key}"
        if raw_value.startswith('"""'):
            remainder = raw_value[3:]
            pieces: list[str] = []
            if remainder:
                if '"""' in remainder:
                    value, trailer = remainder.split('"""', 1)
                    assert not strip_toml_comment(trailer).strip(), (
                        f"content follows multiline TOML string at {path}:{line_number}"
                    )
                    table[key] = value
                    continue
                pieces.append(remainder)
            while index < len(lines) and '"""' not in lines[index]:
                pieces.append(lines[index])
                index += 1
            assert index < len(lines), f"unterminated multiline TOML string at {path}:{line_number}"
            value, trailer = lines[index].split('"""', 1)
            pieces.append(value)
            index += 1
            assert not strip_toml_comment(trailer).strip(), (
                f"content follows multiline TOML string at {path}:{index}"
            )
            table[key] = "\n".join(pieces)
        else:
            table[key] = parse_toml_scalar(raw_value, path, line_number)
    return document


def load_toml_object(path: Path) -> dict[str, Any]:
    if tomllib is not None:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    else:
        data = load_toml_fallback(path)
    assert isinstance(data, dict), f"{path} must contain one TOML object"
    return data


def resolve_local(root: Path, relative: str) -> Path:
    assert isinstance(relative, str) and relative.startswith("./"), f"local path must start ./, got {relative!r}"
    assert not PurePosixPath(relative).is_absolute()
    assert not PureWindowsPath(relative).is_absolute() and not PureWindowsPath(relative).drive
    candidate = (root / relative).resolve()
    assert candidate == root.resolve() or root.resolve() in candidate.parents, f"path escapes package root: {relative}"
    return candidate


def main() -> int:
    codex_config = load_toml_object(CODEX_CONFIG)
    assert codex_config["model"] == TERRA_MODEL, "parent model must remain pinned to Terra"
    agents_config = codex_config.get("agents")
    assert isinstance(agents_config, dict), "Codex config must define the agents table"
    assert agents_config.get("enabled") is True, "custom agents must be enabled"
    assert agents_config.get("max_concurrent_threads_per_session") == 2, (
        "P2 must cap open custom-agent threads at two"
    )
    assert agents_config.get("default_subagent_model") == TERRA_MODEL, (
        "default subagent model must remain pinned to Terra"
    )

    agent_paths = sorted(AGENT_DIRECTORY.glob("*.toml"))
    assert len(agent_paths) == 3, "starter must define exactly three custom agents"
    agents = {path.stem: load_toml_object(path) for path in agent_paths}
    assert set(agents) == {"docs_researcher", "decision_reviewer", "evidence_scout"}
    for stem, agent in agents.items():
        assert agent.get("name") == stem, f"agent name and filename differ: {stem}"
        assert agent.get("model") == TERRA_MODEL, f"{stem} must remain pinned to Terra"
        assert agent.get("sandbox_mode") == "read-only", f"{stem} must remain read-only"
    docs_servers = agents["docs_researcher"].get("mcp_servers")
    assert isinstance(docs_servers, dict), "docs researcher must define an MCP server"
    docs_server = docs_servers.get("openaiDeveloperDocs")
    assert isinstance(docs_server, dict) and docs_server.get("url") == DOCS_MCP_URL, (
        "docs researcher must use the official OpenAI Developer Docs MCP endpoint"
    )

    marketplace = load_object(MARKETPLACE)
    entries = marketplace.get("plugins")
    assert isinstance(entries, list) and len(entries) == 1, "course marketplace must expose exactly one P2 plugin"
    entry = entries[0]
    assert entry["name"] == "p2-release-control"
    assert entry["source"]["source"] == "local"
    resolved_plugin = resolve_local(STARTER, entry["source"]["path"])
    assert resolved_plugin == PLUGIN.resolve(), "marketplace points at the wrong plugin"

    manifest = load_object(PLUGIN / ".codex-plugin/plugin.json")
    assert manifest["name"] == entry["name"], "manifest and marketplace names differ"
    hooks_path = resolve_local(PLUGIN, manifest["hooks"])
    hooks = load_object(hooks_path)
    stop_groups = hooks.get("hooks", {}).get("Stop")
    assert isinstance(stop_groups, list) and len(stop_groups) == 1
    handlers = stop_groups[0].get("hooks")
    assert isinstance(handlers, list) and len(handlers) == 1
    handler = handlers[0]
    assert handler["type"] == "command"
    assert handler["command"] == 'python3 "${PLUGIN_ROOT}/hooks/quality_gate.py"'
    assert handler["commandWindows"] == 'py -3 "%PLUGIN_ROOT%\\hooks\\quality_gate.py"'
    assert (PLUGIN / "hooks/quality_gate.py").is_file()

    contract = load_object(CONTRACT)
    assert contract["enabled"] is False, "starter gate must remain inert until reviewed"
    assert contract["receipt"] == "out/QUALITY_GATE_RECEIPT.json"
    assert REQUIRED_EVIDENCE.issubset(set(contract["required_files"])), "contract omits mandatory release evidence"
    assert REQUIRED_SECRET_PATTERNS.issubset(set(contract["forbidden_patterns"])), "contract omits a course key shape"

    print(
        "PASS p2-release-control package: Codex config, agents, Docs MCP, marketplace, manifest, hook, and contract wiring"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
