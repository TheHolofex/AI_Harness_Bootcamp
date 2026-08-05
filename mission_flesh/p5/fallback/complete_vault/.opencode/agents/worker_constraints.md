---
description: P4 researcher for worker_constraints
mode: subagent
permission:
  "*": deny
  external_directory: deny
  read:
    "*": deny
    "operator/evidence/p4_run_contract.md": allow
    "mission_flesh/p4/raw_corpus/fetched/www_ecfr_gov_current_title_33_c6ea6150fcad.html": allow
    "mission_flesh/p4/raw_corpus/fetched/www_ecfr_gov_current_title_33_c6ea6150fcad.txt": allow
    "mission_flesh/p4/raw_corpus/fetched/www_ecfr_gov_current_title_49_subtitle_B_chapter_III_subchapter_B_part_393_d3a5833bca37.txt": allow
    "mission_flesh/p4/raw_corpus/synthesized/air_contrast/SYN-AIR-0293.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/air_contrast/SYN-AIR-0297.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/air_contrast/SYN-AIR-0299.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/air_contrast/SYN-AIR-0301.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/economic_commercial/SYN-ECO-0314.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/economic_commercial/SYN-ECO-0319.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/economic_commercial/SYN-ECO-0323.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/economic_commercial/SYN-ECO-0326.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/economic_commercial/SYN-ECO-0327.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/economic_commercial/SYN-ECO-0331.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0203.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0214.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0222.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0224.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0228.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0229.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/legal_regulatory/SYN-LEG-0230.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/notices_thin/SYN-NOT-0056.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/notices_thin/SYN-NOT-0409.md": allow
---

# worker_constraints

Read only the allowed assessed-slice source paths.
Return structured JSON to the director.
Do not use the web, MCP, shell, or filesystem write tools.
