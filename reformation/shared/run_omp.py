#!/usr/bin/env python3
"""Run pinned OMP with course-only tools and independently checked receipts.

This is an OMP tool boundary, not an operating-system sandbox. Exit 2 means
invalid invocation/prerequisites; exit 1 preserves an attempted but held run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath

PROVIDER = "openrouter"
MODEL = "anthropic/claude-sonnet-4.6"
SELECTOR = f"{PROVIDER}/{MODEL}"
OMP_VERSION = "omp/18.3.5"
GUARD = Path(__file__).with_name("course_guard.mjs")
DECLARATION = {"schema_version": 1, "yolo": False, "read_root": ".", "write_root": "artifacts", "tools": ["course_read", "course_write"], "skills": False, "gateway": False}
POLICY_KEYS = {"schema_version", "run_id", "work_root", "profile", "tools", "write_files", "write_root", "provider", "model", "omp_version", "prompt_sha256", "instruction", "declaration", "hash_tool", "python", "guard_source_sha256", "runtime_config_sha256", "guard_log", "watch_paths"}
ENV_KEYS = {"PATH", "LANG", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy", "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "NODE_EXTRA_CA_CERTS"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def strict_json(text: str):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid JSON number: {value}")))


def descriptor(value: str | None, label: str, nonempty: bool = True) -> dict | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"missing {label}: {path}")
    raw = path.read_bytes()
    if nonempty and not raw.decode("utf-8").strip():
        raise ValueError(f"empty {label}: {path}")
    return {"path": str(path), "sha256": sha256(raw)}


def overlap(left: Path, right: Path) -> bool:
    return left.is_relative_to(right) or right.is_relative_to(left)


def permission_path(value: str, work: Path) -> str:
    if not value or value in {".", ".."} or "\0" in value or any(char in value for char in ":?#") or Path(value).is_absolute() or PureWindowsPath(value).drive or value.startswith(("\\", "/")):
        raise ValueError(f"permission must be a relative output path: {value!r}")
    pieces = re.split(r"[\\/]", value)
    if any(piece in {"", ".", ".."} for piece in pieces):
        raise ValueError(f"invalid permission path: {value!r}")
    if any(re.fullmatch(r"(?:con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\..*)?", piece, re.I) for piece in pieces):
        raise ValueError("device output paths are not allowed")
    relative = "/".join(pieces)
    target = (work / relative).resolve()
    if not target.is_relative_to(work):
        raise ValueError("permission path escapes through a link")
    return relative


def parse_declaration(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"^```json\s*\n(.*?)^```\s*$", text, re.M | re.S)
    if len(blocks) != 1:
        raise ValueError("AGENT_POLICY.md must contain exactly one JSON block")
    declaration = strict_json(blocks[0])
    if declaration != DECLARATION or set(declaration) != set(DECLARATION) or type(declaration.get("schema_version")) is not int:
        raise ValueError("AGENT_POLICY.md must use the fixed class policy without extra keys or broader permissions")
    return declaration


def isolated_env(runtime: Path, policy: Path, key: str) -> dict[str, str]:
    environment = {name: value for name, value in os.environ.items() if name in ENV_KEYS or name.startswith("LC_")}
    environment["OPENROUTER_API_KEY"] = key
    environment["COURSE_GUARD_POLICY"] = str(policy)
    for name, folder in {"HOME": "home", "USERPROFILE": "home", "APPDATA": "appdata", "LOCALAPPDATA": "localappdata", "XDG_CONFIG_HOME": "config", "XDG_CACHE_HOME": "cache", "XDG_DATA_HOME": "data", "XDG_STATE_HOME": "state", "XDG_RUNTIME_DIR": "xdg-runtime", "TMPDIR": "tmp", "TEMP": "tmp", "TMP": "tmp"}.items():
        target = runtime / folder
        target.mkdir(exist_ok=True)
        environment[name] = str(target)
    return environment


def path_state(path: Path) -> dict:
    if path.is_symlink():
        return {"type": "link", "target": os.readlink(path)}
    if not path.exists():
        return {"type": "missing", "sha256": None}
    if path.is_file():
        return {"type": "file", "sha256": file_hash(path)}
    if path.is_dir():
        return {"type": "directory"}
    raise ValueError(f"unsupported filesystem object: {path}")


def work_snapshot(root: Path) -> dict:
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            result[path.relative_to(root).as_posix()] = path_state(path)
    return dict(sorted(result.items()))


def snapshot(work: Path, watches: list[Path]) -> dict:
    return {"work": work_snapshot(work), "watch": {str(path): path_state(path) for path in watches}}


def read_jsonl(path: Path) -> list[dict]:
    raw = path.read_bytes()
    if not raw or not raw.endswith(b"\n"):
        raise ValueError(f"missing or truncated JSONL: {path.name}")
    rows = []
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            raise ValueError(f"blank JSONL record: {path.name}")
        row = strict_json(line)
        if not isinstance(row, dict) or not isinstance(row.get("type"), str):
            raise ValueError(f"invalid event record: {path.name}")
        rows.append(row)
    return rows


def validate_run(policy: dict, events: list[dict], guard: list[dict], snapshots: dict, child_exit: int) -> list[str]:
    errors = []
    def require(condition, reason):
        if not condition:
            errors.append(reason)
    require(child_exit == 0, f"OMP exited {child_exit}")
    require(set(policy) == POLICY_KEYS and policy.get("schema_version") == 1, "resolved policy schema differs")
    require((policy.get("provider"), policy.get("model"), policy.get("omp_version")) == (PROVIDER, MODEL, OMP_VERSION), "pinned identity differs")
    terminal = [row for row in events if row.get("type") == "agent_end" and row.get("isTerminal") is not False]
    require(len(terminal) == 1, "expected exactly one terminal agent_end")
    require(not any(re.search(r"retry|fallback", row.get("type", "")) or row.get("type") in {"model_changed", "extension_error"} for row in events), "retry, fallback, model drift, or extension error observed")
    require(bool(guard) and guard[0].get("type") == "guard_ready" and guard[-1].get("type") == "guard_end", "guard lifecycle missing or out of order")
    require(sum(row.get("type") == "guard_ready" for row in guard) == 1 and sum(row.get("type") == "guard_end" for row in guard) == 1, "guard lifecycle duplicated or incomplete")
    require(all(row.get("run_id") == policy.get("run_id") for row in guard), "guard run identity differs")
    require(not any(row.get("type") == "guard_error" for row in guard), "guard initialization or identity failed")
    ready = next((row for row in guard if row.get("type") == "guard_ready"), {})
    require(sorted(ready.get("active_tools", [])) == sorted(policy.get("tools", [])), "active tools differ from frozen policy")
    requests = [row for row in guard if row.get("type") == "provider_request"]
    require(bool(requests), "no observed provider request")
    require(all((row.get("provider"), row.get("model")) == (PROVIDER, MODEL) for row in [ready, *requests]), "guard provider/model drift")
    ending = next((row for row in guard if row.get("type") == "guard_end"), {})
    require(ending.get("ready") is True and ending.get("failed") is False, "guard did not finish in a ready, unfailed state")
    require(ending.get("provider_requests") == len(requests), "provider-request count differs")
    if policy.get("instruction"):
        loads = [i for i, row in enumerate(guard) if row.get("type") == "instruction_loaded"]
        first_request = next((i for i, row in enumerate(guard) if row.get("type") == "provider_request"), -1)
        require(bool(loads) and loads[0] < first_request, "saved instruction was not observed before the first request")
        for i in loads:
            row = guard[i]
            require(row.get("file_sha256") == policy["instruction"]["sha256"] and row.get("loaded_text_sha256") == sha256(Path(policy["instruction"]["path"]).read_bytes().decode("utf-8").strip().encode("utf-8")), "loaded instruction identity differs")
    messages = [row.get("message", {}) for row in events if row.get("type") == "message_end"]
    assistants = [message for message in messages if message.get("role") == "assistant"]
    require(bool(assistants) and assistants[-1].get("stopReason") == "stop", "final assistant did not complete normally")
    require(all((message.get("provider"), message.get("model")) == (PROVIDER, MODEL) for message in assistants), "assistant identity drift")
    if terminal and assistants:
        final = [message for message in terminal[0].get("messages", []) if message.get("role") == "assistant"]
        require(bool(final) and final[-1] == assistants[-1], "terminal and streamed assistant records disagree")
    calls, results, starts, ends, decisions, checks, executed, positions = {}, {}, {}, {}, {}, {}, {}, {}
    for message in messages:
        if message.get("role") == "assistant":
            for block in message.get("content", []):
                if block.get("type") == "toolCall":
                    identifier = block.get("id")
                    require(isinstance(identifier, str) and identifier not in calls, "missing or duplicated assistant call ID")
                    calls[identifier] = block
        elif message.get("role") == "toolResult":
            identifier = message.get("toolCallId")
            require(identifier not in results, "duplicated tool result")
            results[identifier] = message
    for row in events:
        if row.get("type") in {"tool_execution_start", "tool_execution_end"}:
            destination = starts if row["type"] == "tool_execution_start" else ends
            identifier = row.get("toolCallId")
            require(identifier not in destination, "duplicated execution event")
            destination[identifier] = row
    for position, row in enumerate(guard):
        if row.get("type") in {"decision", "execution_check", "executed"}:
            destination = {"decision": decisions, "execution_check": checks, "executed": executed}[row["type"]]
            identifier = row.get("call_id")
            require(identifier not in destination, "duplicated guard call record")
            destination[identifier] = row
            positions[(row["type"], identifier)] = position
    require(set(calls) == set(results) == set(starts) == set(ends), "unmatched assistant calls, executions, or results")
    require(set(decisions).issubset(calls) and set(checks).issubset(calls) and set(executed).issubset(calls), "guard record has no actual assistant call")
    writes = {}
    for identifier, call in calls.items():
        start, end, result = starts.get(identifier, {}), ends.get(identifier, {}), results.get(identifier, {})
        require(start.get("toolName") == end.get("toolName") == result.get("toolName") == call.get("name"), "tool name mismatch")
        require(start.get("args") == call.get("arguments"), "tool arguments differ from assistant call")
        require(end.get("isError") == result.get("isError") and end.get("result", {}).get("content") == result.get("content"), "execution/result mismatch")
        decision = decisions.get(identifier)
        if decision:
            require(decision.get("tool") == call.get("name") and decision.get("arguments") == call.get("arguments"), "guard decision does not match call")
            if not decision.get("allow"):
                require(end.get("isError") is True and identifier not in executed, "denied call executed successfully")
        else:
            # Unknown tools are rejected before the extension hook is entered.
            require(call.get("name") not in policy.get("tools", []) and end.get("isError") is True and "not found" in json.dumps(end.get("result", {})).lower(), "call lacks a guard decision or observed runtime rejection")
        if end.get("isError") is False:
            require(identifier in executed and bool(decision and decision.get("allow")), "successful call lacks actual guarded execution")
        if identifier in executed:
            check = checks.get(identifier, {})
            effect = executed[identifier]
            target = Path(effect.get("resolved_path", ""))
            require(call.get("name") in policy["tools"], "executed tool was not declared")
            require(target.is_absolute() and target.is_relative_to(Path(policy["work_root"])), "executed path exceeded the work root")
            require(check.get("allow") is True and check.get("arguments") == call.get("arguments") and check.get("tool") == call.get("name"), "successful execution lacks its independent authorization")
            require(effect.get("tool") == call.get("name") and effect.get("resolved_path") == check.get("resolved_path") == (decision or {}).get("resolved_path"), "executed tool/path differs from its authorization")
            require(positions.get(("decision", identifier), -1) < positions.get(("execution_check", identifier), -1) < positions[("executed", identifier)], "execution preceded its authorization")
            require(end.get("isError") is False, "guard claims execution but runtime reports error")
            if call.get("name") == "course_write":
                writes[executed[identifier].get("resolved_path")] = executed[identifier].get("output_sha256")
    before, after = snapshots["before"], snapshots["after"]
    require(before["watch"] == after["watch"], "watched target changed")
    work = Path(policy["work_root"])
    for relative, old in before["work"].items():
        require(after["work"].get(relative) == old, f"existing input/control changed: {relative}")
    for relative, current in after["work"].items():
        if relative in before["work"]:
            continue
        absolute = str(work / relative)
        if current.get("type") == "directory":
            require(any(Path(output).is_relative_to(work / relative) for output in writes), f"unexplained new directory: {relative}")
        else:
            require(current.get("type") == "file" and writes.get(absolute) == current.get("sha256"), f"unreceipted output or forbidden effect: {relative}")
    for absolute, digest in writes.items():
        target = Path(absolute)
        permitted = target.is_relative_to(work) and (target.relative_to(work).as_posix() in policy["write_files"] or bool(policy["write_root"] and target.is_relative_to(work / policy["write_root"])))
        require(permitted, f"write exceeded policy: {absolute}")
        if target.is_relative_to(work):
            require(after["work"].get(target.relative_to(work).as_posix(), {}).get("sha256") == digest, "tool-written output differs from disk snapshot")
    return errors


def _response_text(events: list[dict]) -> str:
    assistants = [row.get("message", {}) for row in events if row.get("type") == "message_end" and row.get("message", {}).get("role") == "assistant"]
    return "".join(block.get("text", "") for block in (assistants[-1].get("content", []) if assistants else []) if block.get("type") == "text")


def audit_evidence(evidence: Path) -> list[str]:
    """Recheck saved receipts without trusting an assistant's description."""
    try:
        policy = strict_json((evidence / "policy.json").read_text(encoding="utf-8"))
        result = strict_json((evidence / "result.json").read_text(encoding="utf-8"))
        snapshots = strict_json((evidence / "snapshots.json").read_text(encoding="utf-8"))
        events = read_jsonl(evidence / "events.jsonl")
        guard = read_jsonl(evidence / "guard.jsonl")
        errors = validate_run(policy, events, guard, snapshots, result["exit_code"])
        if (evidence / "response.md").read_text(encoding="utf-8") != _response_text(events):
            errors.append("saved response differs from final assistant event")
        expected = {
            "policy_sha256": file_hash(evidence / "policy.json"),
            "guard_sha256": file_hash(evidence / "guard.jsonl"),
            "declared_policy_sha256": policy["declaration"]["sha256"] if policy.get("declaration") else None,
            "instruction_sha256": policy["instruction"]["sha256"] if policy.get("instruction") else None,
            "input_sha256": {name: value["sha256"] for name, value in snapshots["before"]["work"].items() if value["type"] == "file"},
            "output_sha256": {name: value.get("sha256") for name, value in snapshots["after"]["work"].items() if value["type"] == "file" and value != snapshots["before"]["work"].get(name)},
        }
        for key, value in expected.items():
            if result.get(key) != value:
                errors.append(f"{key} differs")
        if (result.get("provider"), result.get("model"), result.get("omp_version")) != (PROVIDER, MODEL, OMP_VERSION):
            errors.append("result provider/model/version differs")
        if result.get("run_id") != policy.get("run_id") or result.get("status") != "PASS":
            errors.append("run identity or completion status differs")
        for row in guard:
            if row.get("type") in {"guard_ready", "guard_end", "instruction_loaded"} and row.get("policy_sha256") != expected["policy_sha256"]:
                errors.append("guard resolved-policy hash differs")
        for key in ("instruction", "declaration"):
            item = policy.get(key)
            if item and file_hash(Path(item["path"])) != item["sha256"]:
                errors.append(f"{key} file changed")
        if file_hash(evidence / "runtime-config.yml") != policy["runtime_config_sha256"]:
            errors.append("runtime overlay changed")
        overlay = strict_json((evidence / "runtime-config.yml").read_text(encoding="utf-8"))
        if overlay.get("retry") != {"enabled": False, "modelFallback": False} or overlay.get("providers", {}).get("cacheWarming") != "off" or overlay.get("tools", {}).get("approval") != {name: "allow" for name in policy["tools"]}:
            errors.append("runtime overlay does not disable retries/fallback/warming and authorize only course tools")
        for path, observed in snapshots["after"]["watch"].items():
            if path_state(Path(path)) != observed:
                errors.append(f"watched target changed after the run: {path}")
        return errors
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
        return [f"incomplete or malformed evidence: {error}"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--instruction")
    access = parser.add_mutually_exclusive_group()
    access.add_argument("--policy")
    access.add_argument("--allow-write", action="append", default=[])
    access.add_argument("--write-root")
    access.add_argument("--hash-tool")
    parser.add_argument("--watch-path", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        work = args.workdir.expanduser().resolve()
        if not work.is_dir():
            raise ValueError(f"missing work directory: {work}")
        evidence_input = args.evidence.expanduser().absolute()
        if evidence_input.exists() or evidence_input.is_symlink():
            raise ValueError(f"evidence attempt already exists: {evidence_input}; choose a new directory")
        evidence = evidence_input.resolve()
        if overlap(work, evidence):
            raise ValueError("work and evidence directories must not overlap")
        prompt = descriptor(args.prompt, "prompt")
        instruction = descriptor(args.instruction, "saved instruction")
        declaration = descriptor(args.policy, "AGENT_POLICY.md")
        hash_tool = descriptor(args.hash_tool, "hash capability")
        write_files = [permission_path(value, work) for value in args.allow_write]
        if len(write_files) != len(set(write_files)):
            raise ValueError("duplicate authorized output")
        if any((work / value).exists() or (work / value).is_symlink() for value in write_files):
            raise ValueError("authorized output already exists; preserve it and choose a new output")
        write_root = permission_path(args.write_root, work) if args.write_root else None
        profile, tools = "read", ["course_read"]
        if declaration:
            parse_declaration(Path(declaration["path"]))
            profile, tools, write_root = "declared", DECLARATION["tools"], "artifacts"
        elif hash_tool:
            if not Path(hash_tool["path"]).is_relative_to(work):
                raise ValueError("hash capability must be the work-copy script")
            profile, tools = "hash", ["course_read", "hash_source"]
        elif write_root or write_files:
            profile, tools = ("write_root" if write_root else "write_files"), ["course_read", "course_write"]
        if write_root:
            permission_path(write_root, work)
            if (work / write_root).exists() and not (work / write_root).is_dir():
                raise ValueError("write root must be a directory")
        watches = [Path(value).expanduser().absolute() for value in args.watch_path]
        if len(watches) != len(set(watches)) or any(path.is_dir() for path in watches):
            raise ValueError("watch paths must be distinct files or missing targets")
        if any(overlap(path.resolve(), evidence) for path in watches):
            raise ValueError("watched targets cannot overlap evidence")
        if not GUARD.is_file():
            raise ValueError("course_guard.mjs is missing; restore the published shared helper")
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if not key:
            raise ValueError("OPENROUTER_API_KEY unavailable; enter and export the key in this terminal")
        omp = shutil.which("omp")
        if not omp:
            raise ValueError("omp is not on PATH; install the pinned verified binary")
    except (OSError, ValueError, UnicodeError) as error:
        print(f"HOLD: {error}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="course-omp-runtime-") as temp:
        runtime = Path(temp).resolve()
        if overlap(runtime, work) or overlap(runtime, evidence):
            print("HOLD: OS temporary directory overlaps work/evidence", file=sys.stderr)
            return 2
        environment = isolated_env(runtime, evidence / "policy.json", key)
        # OMP walks ancestor context files up to HOME even with --no-rules.
        cwd = Path(environment["HOME"]) / "cwd"
        cwd.mkdir()
        try:
            version = subprocess.run([omp, "--version"], cwd=cwd, env=environment, capture_output=True, text=True, timeout=15)
            if version.returncode or version.stdout.strip() != OMP_VERSION:
                raise ValueError(f"require {OMP_VERSION}; pinned executable version did not match")
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            print(f"HOLD: {error}", file=sys.stderr)
            return 2
        evidence.mkdir(parents=True, exist_ok=False)
        overlay = {"retry": {"enabled": False, "modelFallback": False}, "providers": {"cacheWarming": "off"}, "tools": {"approval": {name: "allow" for name in tools}, "intentTracing": False}}
        overlay_file = evidence / "runtime-config.yml"
        overlay_file.write_bytes(json_bytes(overlay))
        policy = {"schema_version": 1, "run_id": str(uuid.uuid4()), "work_root": str(work), "profile": profile, "tools": tools, "write_files": write_files, "write_root": write_root, "provider": PROVIDER, "model": MODEL, "omp_version": OMP_VERSION, "prompt_sha256": prompt["sha256"], "instruction": instruction, "declaration": declaration, "hash_tool": hash_tool, "python": str(Path(sys.executable).resolve()), "guard_source_sha256": file_hash(GUARD), "runtime_config_sha256": file_hash(overlay_file), "guard_log": str(evidence / "guard.jsonl"), "watch_paths": list(map(str, watches))}
        policy_file = evidence / "policy.json"
        policy_file.write_bytes(json_bytes(policy))
        frozen_policy_hash = file_hash(policy_file)
        before = snapshot(work, watches)
        command = [omp, "--model", SELECTOR, "-p", "--mode", "json", "--no-session", "--no-title", "--no-skills", "--no-rules", "--no-extensions", "--no-lsp", "--no-prewalk", "--no-pty", "--max-time", "300", "--approval-mode", "always-ask", "--no-tools", "--tools", ",".join(tools), "--extension", str(GUARD.resolve()), "--config", str(overlay_file)]
        if instruction:
            command.extend(["--append-system-prompt", instruction["path"]])
        started = datetime.now(timezone.utc).isoformat()
        errors = []
        stdout, stderr, child_exit = b"", b"", 1
        try:
            process = subprocess.Popen(command, cwd=cwd, env=environment, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, stderr = process.communicate(Path(prompt["path"]).read_bytes(), timeout=330)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                errors.append("OMP exceeded the 330-second outer deadline")
            child_exit = process.returncode
        except OSError as error:
            errors.append(f"OMP launch failed: {error}")
        if key.encode() in stdout:
            stdout = stdout.replace(key.encode(), b"[REDACTED]")
            errors.append("provider key appeared in stdout; raw stream redacted and held")
        (evidence / "events.jsonl").write_bytes(stdout)
        (evidence / "stderr.txt").write_text(stderr.decode("utf-8", errors="replace").replace(key, "[REDACTED]"), encoding="utf-8")
        after = snapshot(work, watches)
        snapshots = {"before": before, "after": after}
        (evidence / "snapshots.json").write_bytes(json_bytes(snapshots))
        events = []
        try:
            events = read_jsonl(evidence / "events.jsonl")
            guard = read_jsonl(evidence / "guard.jsonl")
            errors.extend(validate_run(policy, events, guard, snapshots, child_exit))
            if any(row.get("policy_sha256") != frozen_policy_hash for row in guard if row.get("type") in {"guard_ready", "guard_end", "instruction_loaded"}):
                errors.append("guard resolved-policy identity differs")
        except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
            errors.append(f"incomplete or malformed receipts: {error}")
        try:
            if file_hash(policy_file) != frozen_policy_hash or file_hash(GUARD) != policy["guard_source_sha256"] or file_hash(overlay_file) != policy["runtime_config_sha256"]:
                errors.append("frozen policy, guard, or configuration changed")
            for item in (prompt, instruction, declaration, hash_tool):
                if item and (not Path(item["path"]).is_file() or file_hash(Path(item["path"])) != item["sha256"]):
                    errors.append("frozen prompt/instruction/declaration/hash capability changed")
        except OSError as error:
            errors.append(f"frozen input could not be rechecked: {error}")
        try:
            response = _response_text(events)
        except (TypeError, AttributeError) as error:
            response = ""
            errors.append(f"malformed final assistant content: {error}")
        (evidence / "response.md").write_text(response, encoding="utf-8")
        result = {"run_id": policy["run_id"], "provider": PROVIDER, "model": MODEL, "omp_version": OMP_VERSION, "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(), "exit_code": child_exit, "policy_sha256": frozen_policy_hash, "guard_sha256": file_hash(evidence / "guard.jsonl") if (evidence / "guard.jsonl").is_file() else None, "declared_policy_sha256": declaration["sha256"] if declaration else None, "instruction_sha256": instruction["sha256"] if instruction else None, "input_sha256": {relative: value["sha256"] for relative, value in before["work"].items() if value["type"] == "file"}, "output_sha256": {relative: value.get("sha256") for relative, value in after["work"].items() if value["type"] == "file" and value != before["work"].get(relative)}, "status": "HOLD" if errors else "PASS", "reason": "; ".join(dict.fromkeys(errors)) if errors else "complete guarded OMP turn; module content still requires its own check"}
        (evidence / "result.json").write_bytes(json_bytes(result))
        print(f"{result['status']}: {result['reason']}")
        return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
