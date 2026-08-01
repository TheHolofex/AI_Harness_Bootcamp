# Usage: python checks_runner.py CHECKS.md answer.txt
# Runs every REQUIRE/FORBID line in CHECKS.md against answer.txt and prints PASS or FAIL for each.

import re
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python checks_runner.py CHECKS.md answer.txt")
        return 2

    checks_path, answer_path = sys.argv[1], sys.argv[2]
    with open(answer_path, encoding="utf-8") as f:
        answer = f.read()

    passed = failed = 0
    with open(checks_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # blank lines and # comment lines are not checks
            parts = line.split(None, 1)
            if len(parts) != 2 or parts[0] not in ("REQUIRE", "FORBID"):
                print(f"SKIP  not a REQUIRE/FORBID line: {line}")
                continue
            kind, pattern = parts
            try:
                found = re.search(pattern, answer) is not None
            except re.error as err:
                print(f"FAIL  {kind} {pattern}  (bad pattern: {err})")
                failed += 1
                continue
            # REQUIRE passes when the pattern is found; FORBID passes when it is not.
            if (kind == "REQUIRE") == found:
                passed += 1
                print(f"PASS  {kind} {pattern}")
            else:
                failed += 1
                print(f"FAIL  {kind} {pattern}")

    print(f"\nTotal: {passed} passed, {failed} failed of {passed + failed} checks")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
