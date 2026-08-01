/**
 * AHB course registry — the single source of truth for Pre-work and B0–P8.
 *
 * Every reader of progress (home dashboard, nav dots, block pages, the
 * pre-work hub) counts against the id lists declared here — never against
 * Object.keys(localStorage) — so stale ids from removed steps (e.g. the
 * deleted `p2-track`) can never inflate a count.
 *
 * Storage: one localStorage key per block, value
 *   { "<check-id>": true, "_updated": ISO }
 * Ids listed in `stretchIds` (stretch exercises, optional tools) never
 * count toward required totals.
 */
(function () {
  "use strict";

  var PULSE_IDS = [
    "pulse-mission", "pulse-log", "pulse-bars",
    "pulse-adv", "pulse-measure", "pulse-transfer"
  ];

  // The detailed checklist rolls up into five outcomes. Explanations and
  // conditional recovery remain on the page but do not block readiness.
  var PREWORK_PHASES = [
    {
      id: "basics", title: "Prepare the machine", time: "45–75 min", anchor: "phase-basics",
      summary: "Confirm the laptop, shell, package manager, Git, Node, and Python.",
      ids: [
        "i-time", "i-log", "i-keys", "b-win11", "b-arm", "b-disk", "b-admin",
        "ps-open", "ps-version", "ps-policy", "wg-check",
        "git-install", "git-restart", "git-verify",
        "np-node", "np-python", "np-restart", "np-verify", "np-stub"
      ]
    },
    {
      id: "keys", title: "Install the keys", time: "20–30 min", anchor: "phase-keys",
      summary: "Store the three course keys safely and prove they survive a fresh shell.",
      ids: ["k-openai", "k-xai", "k-anthropic", "k-models", "k-verify", "sf-make"]
    },
    {
      id: "tools", title: "Prove the required tools", time: "75–120 min", anchor: "phase-tools",
      summary: "Make Codex, OpenCode, Pi, goose, Obsidian, and n8n do observable work.",
      ids: [
        "cx-install", "cx-signin", "cx-status", "cx-lock", "cx-project", "cx-sandbox", "cx-write",
        "oc-version", "oc-install", "oc-verify", "oc-models", "oc-independent", "oc-write",
        "pi-install", "pi-verify", "pi-write", "pi-bash",
        "gs-keyring", "gs-provider", "gs-install", "gs-path", "gs-verify", "gs-write",
        "ob-install", "ob-vault", "n8n-node", "n8n-install", "n8n-start", "n8n-owner", "n8n-stop"
      ]
    },
    {
      id: "files", title: "Open the course files", time: "15–25 min", anchor: "phase-files",
      summary: "Clone the course, find the operator files, and open the local site.",
      ids: ["rp-get", "rp-operator", "rp-site", "rp-gitignore"]
    },
    {
      id: "pack", title: "Pack for Monday", time: "15–20 min", anchor: "phase-pack",
      summary: "Check the four proofs, finish the setup log, and record any clinic item.",
      ids: ["g-four", "g-log", "g-pack"]
    }
  ];

  function preworkRequiredIds() {
    var ids = [];
    PREWORK_PHASES.forEach(function (phase) { ids = ids.concat(phase.ids); });
    return ids;
  }

  // Storage order is retained for compatibility. The visible path is
  // Pre-work → B0 → P1 → … → P8; KEYS is a reference inside Pre-work.
  // `ids` = required ids (mission incl. pulse-brief, the 6 pulse beats, floor).
  var REGISTRY = [
    {
      code: "KEYS", name: "Your API keys", title: "Your API keys", day: "Before Monday", slot: "read",
      key: null, ids: [], stretchIds: [],
      url: "keys.html", meta: "Reference · ~10 min"
    },
    {
      code: "INSTALL", name: "Install + verify as you go", title: "Install + verify as you go", day: "Before Monday", slot: "pre",
      key: "ahb-prework-install",
      ids: preworkRequiredIds(),
      conditionalIds: [
        "i-shape", "wg-fix", "wg-agree", "k-read", "sf-why", "cx-limits",
        "oc-why", "pi-why", "gs-what", "gs-nowinget",
        "r-notfound", "r-window", "r-scripts", "r-auth", "r-store", "r-noclaim", "r-stuck"
      ],
      // Claude Code and the local model are optional — skipping either never
      // blocks the pre-work gate.
      stretchIds: ["cc-optional", "cc-install", "lm-decide", "lm-install", "lm-pull"],
      optionalLabel: "optional",
      url: "checklists/prework-install.html", meta: "Checklist · 2–4 hr"
    },
    {
      code: "B0", name: "Clinic + First Light", title: "Install clinic + First Light", day: "Monday", slot: "AM",
      key: "ahb-checklist-b0",
      ids: [
        "b0-gate", "pulse-brief", "b0-inventory", "b0-build",
        "b0-open", "b0-timeline", "b0-filter", "b0-negative",
        "b0-delta", "b0-loop", "pulse-log", "pulse-bars",
        "pulse-adv", "pulse-measure", "pulse-transfer", "mvp-prework",
        "mvp-brief5", "mvp-four", "mvp-map", "mvp-neg",
        "mvp-upd", "mvp-loop", "mvp-log"
      ],
      stretchIds: [],
      url: "blocks/b0.html", meta: "Codex app"
    },
    {
      code: "P1", name: "Daily Status Brief", title: "The Daily Status Brief", day: "Monday", slot: "PM",
      key: "ahb-checklist-p1",
      ids: [
        "pulse-brief", "p1-corpus", "p1-machine", "p1-regen",
        "p1-audit", "p1-delta", "p1-stale", "p1-judgment",
        "pulse-log", "pulse-bars", "pulse-adv", "pulse-measure",
        "mvp-live", "mvp-rerun", "mvp-5cite", "mvp-delta",
        "mvp-stale", "mvp-own", "p1-transfer"
      ],
      stretchIds: [],
      url: "blocks/p1.html", meta: "Codex app"
    },
    {
      code: "P2", name: "The measured harness", title: "The measured harness", day: "Tuesday", slot: "AM",
      key: "ahb-checklist-p2",
      ids: [
        "pulse-brief", "p2-open", "p2-base", "p2-walls",
        "p2-tests", "p2-after", "p2-durable", "p2-claim",
        "pulse-log", "pulse-bars", "pulse-adv", "pulse-measure",
        "mvp-baseline", "mvp-2walls", "mvp-measure", "mvp-2tests",
        "mvp-cold", "mvp-wallclaim", "mvp-30seed", "p2-transfer"
      ],
      stretchIds: [],
      url: "blocks/p2.html", meta: "Codex · p2_dyno"
    },
    {
      code: "P3", name: "Twin-engine intel desk", title: "The twin-engine intel desk", day: "Tuesday", slot: "PM",
      key: "ahb-checklist-p3",
      ids: [
        "pulse-brief", "p3-brief", "p3-corpus", "p3-codex",
        "p3-claude", "p3-comp", "p3-kill", "p3-note",
        "pulse-log", "pulse-bars", "pulse-adv", "pulse-measure",
        "mvp-briefv1", "mvp-join", "mvp-comp", "mvp-3dis",
        "mvp-kill", "mvp-adj", "mvp-files", "p3-transfer"
      ],
      stretchIds: ["stretch-many-baseline", "stretch-many-minds", "stretch-many-delta", "stretch-worktree"],
      url: "blocks/p3.html", meta: "Codex + OpenCode"
    },
    {
      code: "P4", name: "Director’s second brain", title: "The director’s second brain", day: "Wednesday", slot: "AM",
      key: "ahb-checklist-p4",
      ids: [
        "pulse-brief", "p4-vault", "p4-scope", "p4-inbox",
        "p4-q1", "p4-q2", "p4-audit", "p4-kill",
        "p4-morning", "pulse-log", "pulse-bars", "pulse-adv",
        "pulse-measure", "mvp-scope", "mvp-graph", "mvp-2q",
        "mvp-trail", "mvp-revise", "mvp-morning", "mvp-own4",
        "p4-transfer"
      ],
      stretchIds: [],
      url: "blocks/p4.html", meta: "Codex + Obsidian"
    },
    {
      code: "P5", name: "The poisoned corpus", title: "The poisoned corpus", day: "Wednesday", slot: "PM",
      key: "ahb-checklist-p5",
      ids: [
        "pulse-brief", "p5-boundary", "p5-stage", "p5-false",
        "p5-contra", "p5-hostile", "p5-absent", "p5-perm",
        "p5-rule", "pulse-log", "pulse-bars", "pulse-adv",
        "pulse-measure", "mvp-trusted", "mvp-fc", "mvp-cd",
        "mvp-hi", "mvp-order", "mvp-modes", "mvp-rule",
        "mvp-contain", "p5-transfer"
      ],
      stretchIds: [],
      url: "blocks/p5.html", meta: "Poison pack"
    },
    {
      code: "P6", name: "The watch officer", title: "The watch officer", day: "Thursday", slot: "AM",
      key: "ahb-checklist-p6",
      ids: [
        "pulse-brief", "p6-feeder", "p6-adapt", "p6-contract",
        "p6-stop", "p6-restart", "p6-ex", "p6-sched",
        "p6-pi", "p6-pi-gate", "p6-layers", "pulse-log",
        "pulse-bars", "pulse-adv", "pulse-measure", "mvp-run",
        "mvp-33", "mvp-map", "mvp-stop", "mvp-unatt",
        "mvp-pi", "mvp-ex", "mvp-log6", "mvp-60",
        "p6-transfer"
      ],
      stretchIds: ["stretch-local-predict", "stretch-local-pair", "stretch-local-endpoint"],
      url: "blocks/p6.html", meta: "goose + Pi"
    },
    {
      code: "P7", name: "The automation line", title: "The automation line", day: "Thursday", slot: "PM",
      key: "ahb-checklist-p7",
      ids: [
        "pulse-brief", "p7-rows", "p7-flow", "p7-gate",
        "p7-ex3", "p7-wrong", "p7-disc", "p7-transfer",
        "pulse-log", "pulse-bars", "pulse-adv", "pulse-measure",
        "pulse-transfer", "mvp-e2e", "mvp-gate", "mvp-3ex",
        "mvp-disc", "mvp-slice", "mvp-conf", "mvp-log7",
        "mvp-90"
      ],
      stretchIds: [],
      url: "blocks/p7.html", meta: "n8n + AI step"
    },
    {
      code: "P8", name: "Open model · sealed", title: "Operator-governed open model", day: "Friday", slot: "AM",
      key: "ahb-checklist-p8",
      ids: [
        "pulse-brief", "p8-aup", "p8-repoint", "p8-run",
        "p8-matrix", "p8-layer", "p8-refuse", "p8-defense",
        "p8-seal", "pulse-log", "pulse-bars", "pulse-adv",
        "pulse-measure", "pulse-transfer", "mvp-aup", "mvp-repoint",
        "mvp-hd", "mvp-layer", "mvp-refuse", "mvp-loop8",
        "mvp-90s", "mvp-sealed", "mvp-log8"
      ],
      stretchIds: ["stretch-endpoint-portfolio"],
      url: "blocks/p8.html", meta: "hold/degrade"
    }
  ];

  var COURSE_CODES = ["B0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"];
  var INSTALL = REGISTRY[1];
  var PREWORK_STOP = {
    code: "PREWORK", name: "Mission workstation", title: "Pre-work · Mission workstation",
    day: "Before Monday", slot: "pre", key: INSTALL.key, ids: INSTALL.ids,
    conditionalIds: INSTALL.conditionalIds, stretchIds: INSTALL.stretchIds,
    optionalLabel: INSTALL.optionalLabel, url: "prework.html", meta: "2–4 hr"
  };
  var COURSE_BLOCKS = REGISTRY.filter(function (item) {
    return COURSE_CODES.indexOf(item.code) !== -1;
  });
  var CORE_PATH = [PREWORK_STOP].concat(COURSE_BLOCKS);

  // Journey board columns and day dropdowns are derived from these groups.
  var JOURNEY = [
    { phase: "Before Monday", title: "Pre-work", codes: ["PREWORK"] },
    { phase: "Monday", title: "Foundations", codes: ["B0", "P1"] },
    { phase: "Tuesday", title: "Craft + verdict", codes: ["P2", "P3"] },
    { phase: "Wednesday", title: "Knowledge", codes: ["P4", "P5"] },
    { phase: "Thursday", title: "Autonomy", codes: ["P6", "P7"] },
    { phase: "Friday", title: "Transfer", codes: ["P8"] }
  ];

  var DAY_NAV = [
    { label: "Monday", codes: ["B0", "P1"] },
    { label: "Tuesday", codes: ["P2", "P3"] },
    { label: "Wednesday", codes: ["P4", "P5"] },
    { label: "Thursday", codes: ["P6", "P7"] },
    { label: "Friday", codes: ["P8"] }
  ];

  function block(code) {
    if (code === "PREWORK") return PREWORK_STOP;
    for (var i = 0; i < REGISTRY.length; i++) {
      if (REGISTRY[i].code === code) return REGISTRY[i];
    }
    return null;
  }

  function readState(key) {
    if (!key) return {};
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return {};
      var data = JSON.parse(raw);
      return data && typeof data === "object" ? data : {};
    } catch (e) {
      return {};
    }
  }

  // Required steps done, counted only against the block's declared id list.
  function countDone(b) {
    if (!b || !b.key) return 0;
    var state = readState(b.key);
    var n = 0;
    for (var i = 0; i < b.ids.length; i++) {
      if (state[b.ids[i]] === true) n++;
    }
    return n;
  }

  function countStretchDone(b) {
    if (!b || !b.key || !b.stretchIds.length) return 0;
    var state = readState(b.key);
    var n = 0;
    for (var i = 0; i < b.stretchIds.length; i++) {
      if (state[b.stretchIds[i]] === true) n++;
    }
    return n;
  }

  function isComplete(b) {
    return !!b && b.ids.length > 0 && countDone(b) >= b.ids.length;
  }

  function preworkProgress() {
    var state = readState(INSTALL.key);
    var donePhases = 0;
    var firstPhase = null;
    var firstId = null;
    var phases = PREWORK_PHASES.map(function (phase) {
      var done = 0;
      phase.ids.forEach(function (id) { if (state[id] === true) done++; });
      var complete = done === phase.ids.length;
      if (complete) donePhases++;
      if (!complete && !firstPhase) {
        firstPhase = phase;
        for (var i = 0; i < phase.ids.length; i++) {
          if (state[phase.ids[i]] !== true) { firstId = phase.ids[i]; break; }
        }
      }
      return {
        id: phase.id, title: phase.title, time: phase.time, anchor: phase.anchor,
        summary: phase.summary, done: done, total: phase.ids.length, complete: complete
      };
    });
    return {
      phases: phases, donePhases: donePhases, totalPhases: PREWORK_PHASES.length,
      requiredDone: countDone(INSTALL), requiredTotal: INSTALL.ids.length,
      complete: donePhases === PREWORK_PHASES.length,
      firstPhase: firstPhase, firstId: firstId
    };
  }

  // The current course stop: Pre-work first, then the nine live modules.
  function currentBlock() {
    if (!isComplete(PREWORK_STOP)) return PREWORK_STOP;
    for (var i = 0; i < COURSE_BLOCKS.length; i++) {
      if (!isComplete(COURSE_BLOCKS[i])) return COURSE_BLOCKS[i];
    }
    return COURSE_BLOCKS[COURSE_BLOCKS.length - 1];
  }

  function courseComplete() {
    if (!isComplete(PREWORK_STOP) || !COURSE_BLOCKS.length) return false;
    for (var i = 0; i < COURSE_BLOCKS.length; i++) {
      if (!isComplete(COURSE_BLOCKS[i])) return false;
    }
    return true;
  }

  function moduleNumber(code) {
    return COURSE_CODES.indexOf(code) + 1;
  }

  window.AHB = {
    REGISTRY: REGISTRY,
    JOURNEY: JOURNEY,
    DAY_NAV: DAY_NAV,
    PREWORK_PHASES: PREWORK_PHASES,
    PREWORK_STOP: PREWORK_STOP,
    COURSE_BLOCKS: COURSE_BLOCKS,
    CORE_PATH: CORE_PATH,
    TOTAL_MODULES: COURSE_BLOCKS.length,
    TOTAL_BLOCKS: COURSE_BLOCKS.length,
    block: block,
    readState: readState,
    countDone: countDone,
    countStretchDone: countStretchDone,
    isComplete: isComplete,
    preworkProgress: preworkProgress,
    currentBlock: currentBlock,
    courseComplete: courseComplete,
    moduleNumber: moduleNumber,
    blockNumber: moduleNumber
  };
})();
