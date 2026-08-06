# Human audit sample

| Note | Disposition | Finding |
|---|---|---|
| Notes/Content/Rail_Clearance.md | support | Matches canonical 40 mph and plate guidance |
| Thin corpus notices claiming 45 mph | reject | Contradicts canonical speed; do not promote into spine |
| Notes/Content/Protection_LOC.md | support | Ends in protect/detect/recover language |

## Applied repair

- Repaired path: `Notes/Content/Protection_LOC.md`
- Before: The note described the protection problem but did not close with an explicit recovery action.
- After: The repaired note ends with protect, detect, and recover actions for the affected nodes.
- Expected retrieval effect: A fresh chokepoint-protection query returns all three actions and cites the repaired note.
