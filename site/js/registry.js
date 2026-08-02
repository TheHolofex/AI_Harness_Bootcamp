/**
 * AHB course registry — the single source of truth for B0, B1, the scheduled
 * Model Economics, Harness Control Plane, and MCP briefings, and P1–P8.
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

  // The detailed checklist rolls up into four outcomes. Explanations and
  // conditional recovery remain on the page but do not block readiness.
  var PREWORK_PHASES = [
    {
      id: "basics", title: "Prepare the machine", time: "45–75 min", anchor: "phase-basics",
      summary: "Confirm the laptop and shell, install Git and Node, keep or add one working Python, then clone the course repository.",
      ids: [
        "i-time", "i-keys", "b-win11", "b-arm", "b-disk", "b-admin",
        "ps-open", "ps-version", "ps-policy",
        "git-install", "np-node", "np-python", "git-restart", "git-verify", "rp-get",
        "np-verify", "np-stub"
      ]
    },
    {
      id: "keys", title: "Connect the two keys", time: "15–20 min", anchor: "phase-keys",
      summary: "Keep OpenAI inside Codex, store xAI for every other harness, and verify the shared xAI model pin.",
      ids: ["k-openai", "k-xai", "k-models", "k-verify", "sf-make"]
    },
    {
      id: "tools", title: "Install and verify the course harnesses and tools", time: "75–120 min", anchor: "phase-tools",
      summary: "Install Codex, OpenCode, Pi, goose, Obsidian, and n8n, then verify them with observable work.",
      ids: [
        "cx-install", "cx-signin", "cx-lock", "cx-project", "cx-sandbox", "cx-write",
        "oc-install", "oc-verify", "oc-models", "oc-write",
        "pi-install", "pi-verify", "pi-write", "pi-bash",
        "gs-runtime", "gs-keyring", "gs-provider", "gs-install", "gs-path", "gs-verify", "gs-write",
        "ob-install", "ob-vault", "n8n-install", "n8n-start", "n8n-owner", "n8n-stop",
        "g-four"
      ]
    },
    {
      id: "files", title: "Find the module exercise files", time: "5–10 min", anchor: "phase-files",
      summary: "Find the module missions, supporting instruments, and optional transfer plan.",
      ids: ["rp-operator"]
    }
  ];

  function preworkRequiredIds() {
    var ids = [];
    PREWORK_PHASES.forEach(function (phase) { ids = ids.concat(phase.ids); });
    return ids;
  }

  // Storage order is retained for compatibility. The visible path is
  // B0 install clinic → B1 First Light → Model Economics → P1 →
  // Harness Control Plane → P2 → two MCP briefings → P3 → … → P8.
  // `ids` contains the controls learners can actually see and complete. When an
  // inline lesson outcome replaces a procedural receipt, only the outcome id is
  // required; the duplicate procedural id is retained in the HTML solely so old
  // browser progress can be migrated by shell.js.
  var REGISTRY = [
    {
      code: "KEYS", name: "Your two API keys", title: "Your two API keys", day: "Monday AM", slot: "clinic",
      key: null, ids: [], stretchIds: [],
      url: "keys.html", meta: "Reference · ~10 min"
    },
    {
      code: "INSTALL", name: "Install + verify in clinic", title: "Install + verify in clinic", day: "Monday AM", slot: "clinic",
      key: "ahb-prework-install",
      ids: preworkRequiredIds(),
      conditionalIds: [
        "i-shape", "k-read", "cx-limits",
        "oc-why", "pi-why", "gs-what",
        "r-notfound", "r-window", "r-scripts", "r-auth", "r-store", "r-noclaim", "r-stuck"
      ],
      // The local model is optional — skipping it never blocks the pre-work gate.
      stretchIds: ["lm-decide", "lm-install", "lm-pull"],
      optionalLabel: "optional",
      url: "checklists/prework-install.html", meta: "Monday clinic · 2–4 hr"
    },
    {
      code: "B1", name: "First Light Dashboard", title: "First Light Dashboard", day: "Monday", slot: "AM",
      // Retain the legacy storage bucket name; the simpler B1 workflow uses new outcome ids.
      key: "ahb-checklist-b0",
      ids: ["b1-dashboard", "b1-polish", "b1-verify"],
      stretchIds: [],
      url: "blocks/b1.html", meta: "Codex app"
    },
    {
      code: "ME", name: "Model Economics", title: "Model Economics", kind: "discussion",
      day: "Monday", slot: "PM", key: "ahb-discussion-model-economics",
      ids: ["me-discussed"], stretchIds: [],
      url: "blocks/me.html", meta: "30 min · instructor-led discussion",
      contextLabel: "Monday PM · 30-minute discussion · Before P1"
    },
    {
      code: "P1", name: "Daily Status Brief", title: "The Daily Status Brief", day: "Monday", slot: "PM",
      key: "ahb-checklist-p1",
      ids: [
        "p1-corpus", "p1-machine", "pulse-log", "mvp-live",
        "mvp-rerun", "mvp-5cite", "mvp-delta", "mvp-stale",
        "mvp-own", "p1-transfer"
      ],
      stretchIds: [],
      url: "blocks/p1.html", meta: "Codex app"
    },
    {
      code: "HCP", name: "Skills, hooks, plugins & subagents", title: "Harness Control Plane", kind: "briefing",
      day: "Tuesday", slot: "AM", key: "ahb-briefing-harness-control-plane",
      ids: ["hcp-complete"], stretchIds: [],
      url: "blocks/hcp.html", meta: "30 min · instructor-led presentation",
      contextLabel: "Tuesday AM · 30-minute presentation · Before P2"
    },
    {
      code: "P2", name: "The personal control plane", title: "The personal control plane", day: "Tuesday", slot: "AM",
      key: "ahb-checklist-p2-control-plane",
      ids: [
        "pulse-log", "mvp-control-plane", "mvp-skill", "mvp-plugin",
        "mvp-delegation", "mvp-hook", "mvp-product", "mvp-release",
        "mvp-30seed", "p2-transfer"
      ],
      stretchIds: [],
      url: "blocks/p2.html", meta: "Codex · skills + hooks + plugins + subagents + MCP"
    },
    {
      code: "MCP1", name: "Protocol and production map", title: "MCP & Agent Protocols in Production", kind: "briefing",
      day: "Tuesday", slot: "PM", key: "ahb-briefing-mcp-protocols",
      ids: ["mcp1-complete"], stretchIds: [],
      url: "blocks/mcp1.html", meta: "30 min · instructor-led presentation",
      contextLabel: "Tuesday PM · MCP presentation 1 of 2 · Before P3"
    },
    {
      code: "MCP2", name: "From connection to production", title: "How to Use MCP in 2026", kind: "briefing",
      day: "Tuesday", slot: "PM", key: "ahb-briefing-mcp-practice",
      ids: ["mcp2-complete"], stretchIds: [],
      url: "blocks/mcp2.html", meta: "30 min · instructor-led presentation",
      contextLabel: "Tuesday PM · MCP presentation 2 of 2 · Before P3"
    },
    {
      code: "P3", name: "Twin-engine intel desk", title: "The twin-engine intel desk", day: "Tuesday", slot: "PM",
      key: "ahb-checklist-p3",
      ids: [
        "p3-corpus", "p3-codex", "p3-claude", "mvp-briefv1",
        "mvp-join", "mvp-comp", "mvp-3dis", "mvp-mcp", "mvp-kill",
        "mvp-adj", "mvp-files", "p3-transfer"
      ],
      stretchIds: ["stretch-many-baseline", "stretch-many-minds", "stretch-many-delta"],
      url: "blocks/p3.html", meta: "Codex + OpenCode + bounded MCP"
    },
    {
      code: "P4", name: "Director’s second brain", title: "The director’s second brain", day: "Wednesday", slot: "AM",
      key: "ahb-checklist-p4",
      ids: [
        "pulse-brief", "p4-vault", "p4-q1", "mvp-scope",
        "mvp-graph", "mvp-2q", "mvp-trail", "mvp-revise",
        "mvp-morning", "mvp-own4", "p4-transfer"
      ],
      stretchIds: [],
      url: "blocks/p4.html", meta: "Codex + Obsidian"
    },
    {
      code: "P5", name: "The poisoned corpus", title: "The poisoned corpus", day: "Wednesday", slot: "PM",
      key: "ahb-checklist-p5",
      ids: [
        "pulse-brief", "p5-stage", "p5-hostile", "mvp-trusted",
        "mvp-fc", "mvp-cd", "mvp-hi", "mvp-order",
        "mvp-modes", "mvp-rule", "mvp-contain", "p5-transfer"
      ],
      stretchIds: [],
      url: "blocks/p5.html", meta: "Poison pack"
    },
    {
      code: "P6", name: "The watch officer", title: "The watch officer", day: "Thursday", slot: "AM",
      key: "ahb-checklist-p6",
      ids: [
        "pulse-brief", "p6-feeder", "p6-stop", "p6-layers",
        "mvp-run", "mvp-33", "mvp-map", "mvp-stop",
        "mvp-unatt", "mvp-pi", "mvp-ex", "mvp-log6",
        "mvp-60", "p6-transfer"
      ],
      stretchIds: ["stretch-local-predict", "stretch-local-pair", "stretch-local-endpoint"],
      url: "blocks/p6.html", meta: "goose + Pi"
    },
    {
      code: "P7", name: "The automation line", title: "The automation line", day: "Thursday", slot: "PM",
      key: "ahb-checklist-p7",
      ids: [
        "pulse-brief", "p7-rows", "p7-transfer", "mvp-e2e",
        "mvp-gate", "mvp-3ex", "mvp-disc", "mvp-slice",
        "mvp-conf", "mvp-log7", "mvp-90"
      ],
      stretchIds: [],
      url: "blocks/p7.html", meta: "n8n + AI step"
    },
    {
      code: "P8", name: "Open model · sealed", title: "Operator-governed open model", day: "Friday", slot: "AM",
      key: "ahb-checklist-p8",
      ids: [
        "pulse-brief", "p8-run", "pulse-log", "mvp-aup",
        "mvp-repoint", "mvp-hd", "mvp-layer", "mvp-refuse",
        "mvp-loop8", "mvp-90s", "mvp-sealed"
      ],
      stretchIds: ["stretch-endpoint-portfolio"],
      url: "blocks/p8.html", meta: "hold/degrade"
    }
  ];

  // Nine instructional modules. B0 is the required install-clinic stop before them.
  var COURSE_CODES = ["B1", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"];
  var INSTALL = REGISTRY[1];
  var PREWORK_STOP = {
    code: "B0", name: "Install clinic", title: "Pre-work Install Clinic", kind: "install",
    day: "Monday", slot: "AM", key: INSTALL.key, ids: INSTALL.ids,
    conditionalIds: INSTALL.conditionalIds, stretchIds: INSTALL.stretchIds,
    optionalLabel: INSTALL.optionalLabel, url: "checklists/prework-install.html", meta: "2–4 hr · guided setup"
  };
  var COURSE_BLOCKS = REGISTRY.filter(function (item) {
    return COURSE_CODES.indexOf(item.code) !== -1;
  });
  var NAV_STOPS = REGISTRY.filter(function (item) {
    return COURSE_CODES.indexOf(item.code) !== -1 || item.kind === "discussion" || item.kind === "briefing";
  });
  var CORE_PATH = [PREWORK_STOP].concat(NAV_STOPS);

  // Journey board columns and day dropdowns are derived from these groups.
  var JOURNEY = [
    { phase: "Monday AM", title: "Install Clinic → First Light", codes: ["B0", "B1"] },
    { phase: "Monday PM", title: "Model economics → Daily Status Brief", codes: ["ME", "P1"] },
    { phase: "Tuesday", title: "Control plane → MCP → verdict", codes: ["HCP", "P2", "MCP1", "MCP2", "P3"] },
    { phase: "Wednesday", title: "Knowledge", codes: ["P4", "P5"] },
    { phase: "Thursday", title: "Autonomy", codes: ["P6", "P7"] },
    { phase: "Friday", title: "Transfer", codes: ["P8"] }
  ];

  var DAY_NAV = [
    { label: "Monday", codes: ["B0", "B1", "ME", "P1"] },
    { label: "Tuesday", codes: ["HCP", "P2", "MCP1", "MCP2", "P3"] },
    { label: "Wednesday", codes: ["P4", "P5"] },
    { label: "Thursday", codes: ["P6", "P7"] },
    { label: "Friday", codes: ["P8"] }
  ];

  function block(code) {
    if (code === "PREWORK" || code === "B0") return PREWORK_STOP;
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

  // The current course stop follows the visible path, including briefings,
  // while the numbered module count remains B1 plus P1–P8.
  function currentBlock() {
    for (var i = 0; i < CORE_PATH.length; i++) {
      if (!isComplete(CORE_PATH[i])) return CORE_PATH[i];
    }
    return COURSE_BLOCKS[COURSE_BLOCKS.length - 1];
  }

  function courseComplete() {
    if (!CORE_PATH.length) return false;
    for (var i = 0; i < CORE_PATH.length; i++) {
      if (!isComplete(CORE_PATH[i])) return false;
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
    TOTAL_BLOCKS: CORE_PATH.length,
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
