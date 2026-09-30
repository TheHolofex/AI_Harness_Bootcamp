# Predicate spec

You configure this check. You do not write a second checker.

Input is one run file. The config is a JSON object with one key, `all_present`. That value is a list of exactly two different strings, and neither string may be empty. Any other shape, including an empty list, a duplicate string, an extra key, or a file that is not JSON, is a hold. The check prints `HOLD: malformed config` and does not decide the run.

A **literal** is one of those two strings, matched as written. The match is case-sensitive. Capitals and lowercase are different. The check does not use regular expressions, and it does not evaluate the strings as formulas. It asks only whether each literal occurs somewhere in the file text. A **substring** is enough: the literal may sit inside a longer word.

Both literals present: the process exits 1 and prints `MATCH: both literals present`. Either literal absent: the process exits 0 and prints `PASS: at least one literal absent`. A missing run file exits 1 and prints `HOLD: missing input`. That missing-input line is only for the run file. A bad config uses the malformed-config line instead.

This is a text check, not a release decision. The characters `RELEASED` occur inside `UNRELEASED`, so a config that uses `RELEASED` also matches a hold stamp written as `UNRELEASED`. Measure that limit. Do not treat a match as proof that quality released a cylinder.
