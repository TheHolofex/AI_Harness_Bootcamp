# Desk directory - Task Group MERIDIAN

**Exercise:** NORTHWIND SHELF - TRAINING SYNTHETIC
**Station:** Station Halberd
**Revised:** 2026-06-30

Task Group MERIDIAN is a synthetic composite support group raised for exercise
NORTHWIND SHELF. It runs six desks out of Station Halberd and holds detachments
at Node B, Ferry Point, Bastion Reach and Node D.

| Desk | Head | Capability it holds | Lists it owns |
|---|---|---|---|
| Signals | P-3101 Achebe, N. | SIGNALS | Signals outage recall list |
| Movement | P-3410 Iyer, S. | MOVEMENT | Movement serial nomination list |
| Aid Station | P-3512 Halloran, M. | MEDICAL | Aid station recall list |
| Supply | P-3601 Tan, W. | SUPPLY | (none - handled on the all hands list) |
| Imagery | P-3690 Ferreira, L. | IMAGERY | Imagery tasking list |
| Liaison | P-3755 Marchetti, D. | LIAISON | (none - handled on the all hands list) |
| Adjutant's cell | P-3410 Iyer, S. (dual-hatted) | - | All hands list |

## Capabilities recognised by the group

`SIGNALS` `MOVEMENT` `MEDICAL` `SUPPLY` `IMAGERY` `LIAISON`

A person holds a capability by billet or by qualification, not by which desk
they report to. A gaining desk is an address, not a trade.

## Where capability is written down

| Record | Holds | Kept by |
|---|---|---|
| `records/billet_catalog.csv` | billet code to capability, with a revision date | Adjutant's cell |
| `records/qualification_register.csv` | person to qualification, with grant, expiry and status | the awarding desk |
| `records/current_roster.csv` | who is on station and against which billet | Adjutant's cell |
| `records/rotation_out.csv` | last duty day and destination for people leaving | Adjutant's cell |

Billet codes are issued by the Adjutant's cell as posts are stood up. The
catalog is revised quarterly, so a code cut after the last revision will not
appear in it.

Qualification status is one of `current`, `expired` or `pending`. `pending`
means an application is with the awarding desk and nothing has been granted.
