# Design: website-first day path

## Learner path

The website is the complete visible learner surface. The primary route is:

`Home → Pre-work → Monday B0 → Monday P1 → Tuesday P2 → Tuesday P3 → Wednesday P4 → Wednesday P5 → Thursday P6 → Thursday P7 → Friday P8`

The brand remains the home link. Primary navigation contains only `Pre-work`, `Mon`, `Tue`, `Wed`, `Thu`, and `Fri`. Day menus expose their one or two modules and progress state. Resources, instruments, operator references, and lead material do not appear in primary navigation.

## Content disposition

- A visible link may never open raw Markdown.
- If the linked source repeats content already on the module page, remove the link and point to the local section.
- If the linked source is needed repeatedly during the course, represent it as a web reference page.
- If it is a working file in the cloned course pack, show its path as code text beside the action that needs it; do not make the path a web link.
- If it is optional practice, keep the HTML handout beside its owning module, label it optional, state its time cost, and make the owning module the dominant return route.
- Staff/source documents remain outside the visible learner surface.

## Navigation and progress

- Pre-work is a prerequisite, not “Block 1.” The contact course is nine modules, B0 through P8.
- Module context labels use day, slot, and `Module N of 9`.
- Previous/next controls follow the learner path; Pre-work precedes B0.
- Existing local-storage keys and still-valid check IDs remain compatible.
- Conditional repair and troubleshooting checks do not count toward pre-work completion.
- The pre-work page exposes a short phase map and a first-incomplete resume target.

## Handout boundary

Handouts remain reachable from contextual “Optional field guide” links in their owning module. Their page header and footer route back to that module. Shelf-to-shelf browsing and the global resource hub remain secondary and are not part of course navigation.

## Compatibility

Published HTML URLs remain in place. Existing checklist redirect stubs continue to send learners to the owning module. The current static HTML/CSS/JavaScript architecture and Starzl visual system remain unchanged.

## Validation contract

- zero visible `href` values ending in `.md` anywhere under `site/`
- primary nav contains only Pre-work and Monday–Friday
- B0–P8 report `Module 1 of 9` through `Module 9 of 9`
- every local link and fragment resolves
- generated resources rebuild deterministically and return to their owner module
- pre-work completion excludes conditional recovery work
- JavaScript and Python syntax checks pass
- the site works when `site/` alone is used as a static document root

