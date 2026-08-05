---
description: P4 researcher for worker_conus_rail_road
mode: subagent
permission:
  "*": deny
  external_directory: deny
  read:
    "*": deny
    "operator/evidence/p4_run_contract.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0005.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0008.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0020.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0021.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0335.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0339.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0349.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0350.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0356.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/movement_doctrine/SYN-MOV-0357.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0030.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0032.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0033.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0034.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0035.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0037.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0038.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0044.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0046.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0050.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0053.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/rail/SYN-RAI-0054.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0064.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0069.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0070.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0071.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0073.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0074.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0085.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0088.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0090.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/road/SYN-ROA-0091.md": allow
---

# worker_conus_rail_road

Read only the allowed assessed-slice source paths.
Return structured JSON to the director.
Do not use the web, MCP, shell, or filesystem write tools.
