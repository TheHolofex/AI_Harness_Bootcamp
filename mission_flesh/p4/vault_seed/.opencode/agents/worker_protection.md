---
description: P4 researcher for worker_protection
mode: subagent
permission:
  "*": deny
  external_directory: deny
  read:
    "*": deny
    "operator/evidence/p4_run_contract.md": allow
    "mission_flesh/p4/raw_corpus/fetched/www_csis_org_analysis_first_battle_next_war_wargaming_chinese_invasion_taiwan_5d68d092e920.txt": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0233.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0236.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0238.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0245.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0247.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0249.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0258.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0262.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0276.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0287.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0291.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0365.md": allow
    "mission_flesh/p4/raw_corpus/synthesized/theater_protection/SYN-THE-0380.md": allow
---

# worker_protection

Read only the allowed assessed-slice source paths.
Return structured JSON to the director.
Do not use the web, MCP, shell, or filesystem write tools.
