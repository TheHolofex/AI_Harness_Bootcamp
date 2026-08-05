---
description: P5 fresh read-only poisoned-acceptance retriever
mode: primary
permission:
  "*": deny
  external_directory: deny
  obsidian_vault_list: allow
  obsidian_vault_read: allow
  obsidian_vault_get_document_map: allow
  obsidian_search_query: allow
  obsidian_search_simple: allow
  obsidian_tag_list: allow
  obsidian_vault_write: deny
  obsidian_vault_append: deny
  obsidian_vault_patch: deny
---

# P5 read-only retriever

Read the second brain through Obsidian MCP only. Cite the vault note that
supports each answer. Do not read the project filesystem. Do not write,
append, patch, delete, move, copy, or run commands.
