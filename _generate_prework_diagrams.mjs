import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const OUT = path.join(ROOT, "site/assets/prework");
const TMP = "/tmp/prework-diagrams";

fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(TMP, { recursive: true });

const C = {
  paper: "#FFFFFF",
  warm: "#FAFAF8",
  panel: "#F4F4F2",
  ink: "#0A0A0A",
  muted: "#4A4A4A",
  faint: "#6B6B6B",
  rule: "#D0D0D0",
  strong: "#1A1A1A",
  mark: "#E31C23",
  gold: "#A58650",
};

const installStages = [
  "BYB",
  "0 Base",
  "1 Term",
  "2 winget",
  "3 Git",
  "4 Runtime",
  "5 Keys",
  "6 Smoke",
  "7 Codex",
  "8 OpenCode",
  "9 Pi",
  "10 goose",
  "11 Obsidian",
  "12 n8n",
  "13 Repo",
  "14 Claude*",
  "15 Gate",
];

const healthStages = [
  "Run",
  "A Found",
  "B Keys",
  "C Agents",
  "D Support",
  "E Ready",
  "Result",
];

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function svgOpen(title, height) {
  const titleId = `title-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 ${height}" role="img" aria-labelledby="${titleId}">
  <title id="${titleId}">${esc(title)}</title>
  <defs>
    <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 8 4 0 8Z" fill="${C.ink}"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 8 4 0 8Z" fill="${C.mark}"/>
    </marker>
    <style>
      text { font-family: system-ui, "Inter", "Helvetica Neue", Arial, sans-serif; fill: ${C.ink}; }
      .micro { font-size: 8px; font-weight: 650; letter-spacing: 1.65px; }
      .tiny { font-size: 7px; font-weight: 650; letter-spacing: 1px; }
      .railtext { font-size: 7.1px; font-weight: 650; }
      .title { font-size: 21px; font-weight: 680; letter-spacing: -0.25px; }
      .purpose { font-size: 11.5px; font-weight: 430; fill: ${C.muted}; }
      .caption { font-size: 8.5px; font-weight: 650; letter-spacing: 1.15px; }
      .body { font-size: 9.5px; font-weight: 520; }
      .muted { fill: ${C.faint}; }
      .white { fill: ${C.paper}; }
      .red { fill: ${C.mark}; }
      .gold { fill: ${C.gold}; }
      .line { fill: none; stroke: ${C.ink}; stroke-width: 1.35; vector-effect: non-scaling-stroke; }
      .hair { fill: none; stroke: ${C.rule}; stroke-width: 1; vector-effect: non-scaling-stroke; }
      .redline { fill: none; stroke: ${C.mark}; stroke-width: 1.4; vector-effect: non-scaling-stroke; }
      .goldline { fill: none; stroke: ${C.gold}; stroke-width: 1.35; vector-effect: non-scaling-stroke; }
      .dash { stroke-dasharray: 5 4; }
    </style>
  </defs>
  <rect width="1120" height="${height}" fill="${C.paper}"/>
`;
}

function ribbon(kind, current, { overview = false, crosscut = false } = {}) {
  const install = kind === "install";
  const stages = install ? installStages : healthStages;
  const label = install ? "PRE-WORK · INSTALL PATH" : "PRE-WORK · HEALTH GATE";
  const start = install ? 24 : 28;
  const width = install ? 58 : 138;
  const gap = install ? 5 : 18;
  const y = 25;
  const h = 24;
  const end = start + (stages.length - 1) * (width + gap) + width;
  const progress = crosscut
    ? "RECOVERY · ANY STAGE"
    : overview
      ? "FULL JOURNEY"
      : `STAGE ${String(current + 1).padStart(2, "0")} OF ${String(stages.length).padStart(2, "0")}`;
  let result = `  <rect x="0" y="0" width="1120" height="56" fill="${C.warm}"/>
  <text x="24" y="13" class="micro muted">${label}</text>
  <text x="1096" y="13" class="micro ${crosscut ? "red" : "muted"}" text-anchor="end">${progress}</text>
  <path d="M${start + width / 2} 37H${end - width / 2}" class="hair"/>
`;
  stages.forEach((stage, index) => {
    const x = start + index * (width + gap);
    const optional = install && index === 15;
    const completed = !overview && !crosscut && index < current;
    const active = !overview && !crosscut && index === current;
    const stroke = optional ? C.gold : active ? C.mark : C.rule;
    const fill = active && !optional ? C.mark : C.paper;
    const strokeWidth = active || optional ? 1.4 : 1;
    result += `  <rect x="${x}" y="${y}" width="${width}" height="${h}" rx="2" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"/>
`;
    if (completed) {
      result += `  <circle cx="${x + 7}" cy="${y + 12}" r="2.6" fill="${C.mark}"/>
  <text x="${x + width / 2 + 3}" y="${y + 15}" class="railtext" text-anchor="middle">${esc(stage)}</text>
`;
    } else {
      const textClass = active && !optional ? "railtext white" : optional ? "railtext gold" : "railtext muted";
      result += `  <text x="${x + width / 2}" y="${y + 15}" class="${textClass}" text-anchor="middle">${esc(stage)}</text>
`;
    }
    if (active && optional) {
      result += `  <path d="M${x + 1} ${y + 2}H${x + width - 1}" class="goldline"/>
`;
    }
  });
  if (overview) {
    result += `  <circle cx="${start + 7}" cy="37" r="2.6" fill="${C.mark}"/>
  <text x="${start + 15}" y="53" class="tiny red">START</text>
`;
  }
  if (crosscut) {
    result += `  <path d="M${start} 52V54H${end}V52" class="redline"/>
`;
  }
  result += `  <path d="M0 56H1120" class="hair"/>
`;
  return result;
}

function chips(items, accent = C.ink) {
  const left = 24;
  const right = 1096;
  const gap = 8;
  const width = (right - left - gap * (items.length - 1)) / items.length;
  let result = `  <rect x="0" y="164" width="1120" height="56" fill="${C.warm}"/>
  <text x="24" y="175" class="micro muted">SECTION RUN</text>
`;
  items.forEach((item, index) => {
    const x = left + index * (width + gap);
    result += `  <rect x="${x.toFixed(2)}" y="182" width="${width.toFixed(2)}" height="25" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
  <rect x="${x.toFixed(2)}" y="182" width="25" height="25" rx="2" fill="${accent}"/>
  <text x="${(x + 12.5).toFixed(2)}" y="198.3" class="caption white" text-anchor="middle">${String(index + 1).padStart(2, "0")}</text>
  <text x="${(x + 34).toFixed(2)}" y="198.2" class="caption">${esc(item)}</text>
`;
  });
  return result;
}

function middleHeader(stage, purpose, kind, optional = false) {
  const eyebrow = kind === "install" ? "INSTALL STAGE" : "HEALTH STAGE";
  return `  <text x="24" y="76" class="micro ${optional ? "gold" : "red"}">${eyebrow}</text>
  <text x="24" y="103" class="title">${esc(stage)}</text>
  <text x="24" y="123" class="purpose">${esc(purpose)}</text>
  <path d="M480 69V151" class="hair"/>
  <text x="512" y="76" class="micro muted">STAGE VIEW</text>
`;
}

function sectionSvg(kind, config) {
  const accent = config.optional ? C.gold : C.ink;
  return `${svgOpen(config.svgTitle, 220)}${ribbon(kind, config.current, { crosscut: config.crosscut })}${middleHeader(config.stage, config.purpose, kind, config.optional)}${config.metaphor}${chips(config.steps, accent)}</svg>
`;
}

const metaphor = {
  begin: `  <g aria-label="Calendar, setup log, and three key marks">
    <rect x="540" y="86" width="92" height="57" rx="2" fill="${C.panel}" stroke="${C.strong}"/>
    <path d="M540 101H632M558 82V93M614 82V93" class="line"/>
    <rect x="553" y="112" width="13" height="10" fill="${C.mark}"/>
    <rect x="572" y="112" width="13" height="10" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="591" y="112" width="13" height="10" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="586" y="137" class="tiny muted" text-anchor="middle">TIME BLOCK</text>
    <path d="M656 76H741L756 91V145H656Z" fill="${C.paper}" stroke="${C.strong}"/>
    <path d="M741 76V91H756M670 102H737M670 113H737M670 124H720" class="hair"/>
    <path d="M670 134l4 4 7-9" class="redline"/>
    <text x="706" y="93" class="tiny muted" text-anchor="middle">SETUP LOG</text>
    <path d="M786 99H1063" class="hair"/>
    <rect x="800" y="87" width="77" height="27" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="810" cy="100.5" r="4" fill="${C.mark}"/>
    <text x="838" y="104" class="caption" text-anchor="middle">OPENAI</text>
    <rect x="892" y="87" width="77" height="27" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="902" cy="100.5" r="4" fill="${C.mark}"/>
    <text x="930" y="104" class="caption" text-anchor="middle">XAI</text>
    <rect x="984" y="87" width="91" height="27" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="994" cy="100.5" r="4" fill="${C.mark}"/>
    <text x="1031" y="104" class="caption" text-anchor="middle">ANTHROPIC</text>
    <text x="937" y="136" class="tiny muted" text-anchor="middle">THREE KEYS IN HAND</text>
  </g>
`,
  baseline: `  <g aria-label="Windows laptop and disk capacity gauge">
    <rect x="550" y="82" width="205" height="60" rx="3" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="559" y="90" width="187" height="43" fill="${C.panel}" stroke="${C.rule}"/>
    <path d="M530 146H775L758 153H547Z" fill="${C.panel}" stroke="${C.strong}"/>
    <rect x="574" y="100" width="48" height="22" rx="2" fill="${C.ink}"/>
    <text x="598" y="114.5" class="caption white" text-anchor="middle">WIN 11</text>
    <text x="690" y="107" class="micro muted" text-anchor="middle">SYSTEM TYPE</text>
    <text x="690" y="122" class="caption" text-anchor="middle">64-BIT · AMD64</text>
    <circle cx="856" cy="116" r="38" fill="${C.warm}" stroke="${C.rule}"/>
    <path d="M829 136A32 32 0 1 1 882 136" class="line"/>
    <path d="M856 116L878 96" class="redline"/>
    <circle cx="856" cy="116" r="3" fill="${C.mark}"/>
    <text x="856" y="141" class="caption" text-anchor="middle">25+ GB</text>
    <rect x="930" y="87" width="137" height="57" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="998.5" y="104" class="micro muted" text-anchor="middle">INSTALL RIGHTS</text>
    <path d="M960 124H1037" class="hair"/>
    <circle cx="975" cy="124" r="7" fill="${C.mark}"/>
    <path d="M971 124l3 3 6-7" fill="none" stroke="${C.paper}" stroke-width="1.4"/>
    <text x="1011" y="128" class="caption" text-anchor="middle">KNOWN</text>
  </g>
`,
  terminal: `  <g aria-label="PowerShell and Bash terminal panes">
    <rect x="530" y="82" width="242" height="66" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="530" y="82" width="242" height="18" fill="${C.panel}" stroke="${C.strong}"/>
    <circle cx="542" cy="91" r="2.5" fill="${C.mark}"/>
    <text x="653" y="94" class="tiny muted" text-anchor="middle">POWERSHELL</text>
    <text x="545" y="118" class="body red">PS&gt;</text>
    <path d="M569 119H663" class="line"/>
    <rect x="668" y="110" width="7" height="12" fill="${C.ink}"/>
    <text x="545" y="138" class="tiny muted">CURRENTUSER · REMOTESIGNED</text>
    <path d="M793 115H829" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="847" y="82" width="221" height="66" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="847" y="82" width="221" height="18" fill="${C.panel}" stroke="${C.rule}"/>
    <text x="957.5" y="94" class="tiny muted" text-anchor="middle">GIT BASH · NEXT STAGE</text>
    <text x="862" y="120" class="body">$</text>
    <path d="M878 119H952" class="line"/>
    <text x="862" y="138" class="tiny muted">FRESH WINDOW · FRESH PATH</text>
  </g>
`,
  winget: `  <g aria-label="Package box moving along an install conveyor">
    <path d="M545 137H1068" class="line" marker-end="url(#arrow)"/>
    <circle cx="590" cy="137" r="8" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="1015" cy="137" r="8" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="678" y="82" width="128" height="56" rx="2" fill="${C.panel}" stroke="${C.strong}"/>
    <path d="M678 98L742 116 806 98M742 116V138M678 82L742 100 806 82" class="line"/>
    <text x="742" y="94" class="caption" text-anchor="middle">WINGET</text>
    <rect x="842" y="89" width="180" height="36" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="860" cy="107" r="7" fill="${C.mark}"/>
    <path d="M856 107l3 3 6-7" fill="none" stroke="${C.paper}" stroke-width="1.4"/>
    <text x="938" y="104" class="tiny muted" text-anchor="middle">SOURCE TERMS</text>
    <text x="938" y="116" class="caption" text-anchor="middle">ACCEPTED</text>
    <text x="574" y="104" class="tiny muted" text-anchor="middle">FIND</text>
    <text x="1050" y="104" class="tiny muted" text-anchor="middle">INSTALL</text>
  </g>
`,
  git: `  <g aria-label="Git commit graph">
    <path d="M558 112H690C724 112 724 87 758 87H882C916 87 916 123 950 123H1067" class="line"/>
    <path d="M690 112C724 112 724 140 758 140H878C912 140 912 123 950 123" class="redline"/>
    <circle cx="558" cy="112" r="8" fill="${C.ink}"/>
    <circle cx="690" cy="112" r="7" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="758" cy="87" r="7" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="758" cy="140" r="7" fill="${C.mark}"/>
    <circle cx="882" cy="87" r="7" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="950" cy="123" r="8" fill="${C.ink}"/>
    <circle cx="1067" cy="123" r="7" fill="${C.paper}" stroke="${C.strong}"/>
    <text x="558" y="94" class="tiny muted" text-anchor="middle">INSTALL</text>
    <text x="758" y="155" class="tiny red" text-anchor="middle">GIT BASH</text>
    <text x="950" y="105" class="tiny muted" text-anchor="middle">VERIFY</text>
  </g>
`,
  runtime: `  <g aria-label="Node.js and Python runtime badges">
    <path d="M530 115H1072" class="hair"/>
    <rect x="566" y="82" width="202" height="66" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="566" y="82" width="12" height="66" fill="${C.mark}"/>
    <text x="603" y="105" class="micro muted">RUNTIME A</text>
    <text x="603" y="129" class="title">NODE LTS</text>
    <rect x="808" y="82" width="202" height="66" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="998" y="82" width="12" height="66" fill="${C.ink}"/>
    <text x="832" y="105" class="micro muted">RUNTIME B</text>
    <text x="832" y="129" class="title">PYTHON</text>
    <circle cx="789" cy="115" r="8" fill="${C.panel}" stroke="${C.rule}"/>
    <text x="789" y="118" class="caption" text-anchor="middle">+</text>
    <text x="1055" y="104" class="tiny muted" text-anchor="middle">FRESH PATH</text>
    <path d="M1028 115H1080" class="redline" marker-end="url(#arrow-red)"/>
  </g>
`,
  keys: `  <g aria-label="Three sealed provider key tags">
    <path d="M548 85H1060" class="hair"/>
    <rect x="558" y="88" width="150" height="54" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="580" cy="115" r="9" fill="${C.mark}"/>
    <path d="M589 115H605M600 115V121M605 115V119" class="line"/>
    <text x="654" y="111" class="micro muted" text-anchor="middle">OPENAI</text>
    <text x="654" y="127" class="caption" text-anchor="middle">USER VARIABLE</text>
    <rect x="729" y="88" width="150" height="54" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="751" cy="115" r="9" fill="${C.mark}"/>
    <path d="M760 115H776M771 115V121M776 115V119" class="line"/>
    <text x="825" y="111" class="micro muted" text-anchor="middle">XAI</text>
    <text x="825" y="127" class="caption" text-anchor="middle">USER VARIABLE</text>
    <rect x="900" y="88" width="166" height="54" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="922" cy="115" r="9" fill="${C.mark}"/>
    <path d="M931 115H947M942 115V121M947 115V119" class="line"/>
    <text x="998" y="111" class="micro muted" text-anchor="middle">ANTHROPIC</text>
    <text x="998" y="127" class="caption" text-anchor="middle">USER VARIABLE</text>
    <path d="M558 149H1066" class="redline"/>
    <text x="812" y="158" class="tiny red" text-anchor="middle">VERIFY IN A BRAND-NEW WINDOW</text>
  </g>
`,
  smoke: `  <g aria-label="Shared smoke folder with four proof-file slots">
    <path d="M564 90H715L733 105H1059V149H564Z" fill="${C.warm}" stroke="${C.strong}"/>
    <text x="595" y="115" class="micro muted">PREWORK-SMOKE</text>
    <rect x="742" y="111" width="68" height="26" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="823" y="111" width="68" height="26" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="904" y="111" width="68" height="26" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="985" y="111" width="61" height="26" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="776" y="127" class="tiny muted" text-anchor="middle">CODEX</text>
    <text x="857" y="127" class="tiny muted" text-anchor="middle">OPEN</text>
    <text x="938" y="127" class="tiny muted" text-anchor="middle">PI</text>
    <text x="1015.5" y="127" class="tiny muted" text-anchor="middle">GOOSE</text>
    <circle cx="776" cy="145" r="3" fill="${C.mark}"/>
    <circle cx="857" cy="145" r="3" fill="${C.mark}"/>
    <circle cx="938" cy="145" r="3" fill="${C.mark}"/>
    <circle cx="1015.5" cy="145" r="3" fill="${C.mark}"/>
    <text x="679" y="137" class="caption" text-anchor="middle">ONE BAY</text>
  </g>
`,
  codex: `  <g aria-label="Codex primary engine home base">
    <path d="M547 104L592 78H735L780 104V147H547Z" fill="${C.warm}" stroke="${C.strong}"/>
    <rect x="582" y="99" width="163" height="36" rx="2" fill="${C.ink}"/>
    <circle cx="602" cy="117" r="6" fill="${C.mark}"/>
    <text x="667" y="113" class="micro white" text-anchor="middle">CODEX</text>
    <text x="667" y="127" class="tiny white" text-anchor="middle">PRIMARY ENGINE · HOME</text>
    <path d="M780 117H842" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="859" y="80" width="199" height="68" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <path d="M859 103H1058M925 103V148M992 103V148" class="hair"/>
    <text x="958.5" y="95" class="micro muted" text-anchor="middle">CONTROL PLANE</text>
    <text x="892" y="120" class="tiny muted" text-anchor="middle">API KEY</text>
    <text x="958.5" y="120" class="tiny muted" text-anchor="middle">SANDBOX</text>
    <text x="1025" y="120" class="tiny muted" text-anchor="middle">PROOF</text>
    <circle cx="892" cy="135" r="4" fill="${C.mark}"/>
    <circle cx="958.5" cy="135" r="4" fill="${C.ink}"/>
    <circle cx="1025" cy="135" r="4" fill="${C.mark}"/>
  </g>
`,
  opencode: `  <g aria-label="Twin primary and second engines">
    <rect x="548" y="86" width="205" height="58" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="548" y="86" width="11" height="58" fill="${C.ink}"/>
    <text x="579" y="105" class="micro muted">ENGINE 01 · HOME</text>
    <text x="579" y="130" class="title">CODEX</text>
    <path d="M777 115H829" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="846" y="78" width="221" height="74" rx="2" fill="${C.ink}" stroke="${C.ink}"/>
    <rect x="846" y="78" width="11" height="74" fill="${C.mark}"/>
    <text x="878" y="101" class="micro white">ENGINE 02 · XAI</text>
    <text x="878" y="130" class="title white">OPENCODE</text>
    <text x="1060" y="71" class="tiny red" text-anchor="end">COHORT PIN</text>
  </g>
`,
  pi: `  <g aria-label="Minimal agent loop">
    <circle cx="805" cy="116" r="52" fill="${C.warm}" stroke="${C.rule}"/>
    <path d="M805 72A44 44 0 1 1 767 94" class="redline" marker-end="url(#arrow-red)"/>
    <circle cx="805" cy="116" r="23" fill="${C.paper}" stroke="${C.strong}"/>
    <text x="805" y="121" class="title" text-anchor="middle">π</text>
    <rect x="548" y="92" width="116" height="46" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="606" y="111" class="micro muted" text-anchor="middle">PROMPT</text>
    <text x="606" y="126" class="caption" text-anchor="middle">INPUT</text>
    <rect x="946" y="92" width="116" height="46" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="1004" y="111" class="micro muted" text-anchor="middle">SHELL</text>
    <text x="1004" y="126" class="caption" text-anchor="middle">REACH</text>
    <path d="M664 115H738M872 115H946" class="line"/>
    <text x="805" y="158" class="tiny red" text-anchor="middle">PROMPT → TOOL → OUTPUT → LOOP</text>
  </g>
`,
  goose: `  <g aria-label="Bounded work recipe and completion stamp">
    <rect x="555" y="76" width="303" height="78" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="555" y="76" width="303" height="19" fill="${C.panel}" stroke="${C.strong}"/>
    <text x="706.5" y="89" class="micro muted" text-anchor="middle">BOUNDED RECIPE</text>
    <path d="M575 108h8v8h-8zM575 126h8v8h-8z" fill="${C.paper}" stroke="${C.strong}"/>
    <path d="M576 111l3 3 7-8M576 129l3 3 7-8" class="redline"/>
    <text x="598" y="115" class="body">PROVIDER + MODEL</text>
    <text x="598" y="133" class="body">PATH + KEYRING</text>
    <path d="M858 115H900" class="redline" marker-end="url(#arrow-red)"/>
    <circle cx="974" cy="115" r="48" fill="${C.warm}" stroke="${C.gold}" stroke-width="1.5"/>
    <circle cx="974" cy="115" r="37" fill="${C.paper}" stroke="${C.rule}"/>
    <path d="M953 115l13 13 28-32" fill="none" stroke="${C.mark}" stroke-width="2.2"/>
    <text x="974" y="150" class="tiny gold" text-anchor="middle">REPEATABLE</text>
  </g>
`,
  obsidian: `  <g aria-label="Obsidian vault diamond and note graph">
    <path d="M626 72L704 115 626 158 548 115Z" fill="${C.warm}" stroke="${C.strong}"/>
    <path d="M626 84L682 115 626 146 570 115Z" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="626" y="112" class="micro muted" text-anchor="middle">LOCAL</text>
    <text x="626" y="128" class="caption" text-anchor="middle">VAULT</text>
    <path d="M704 115H780M805 88L882 115 805 143M882 115L984 86M882 115L984 145M984 86L1052 115M984 145L1052 115" class="hair"/>
    <circle cx="805" cy="88" r="8" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="805" cy="143" r="8" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="882" cy="115" r="9" fill="${C.mark}"/>
    <circle cx="984" cy="86" r="8" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="984" cy="145" r="8" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="1052" cy="115" r="8" fill="${C.ink}"/>
    <text x="930" y="73" class="tiny muted" text-anchor="middle">NOTE GRAPH</text>
  </g>
`,
  n8n: `  <g aria-label="Local n8n node workflow">
    <path d="M565 116H1054" class="hair"/>
    <rect x="552" y="94" width="110" height="44" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="571" cy="116" r="6" fill="${C.mark}"/>
    <text x="615" y="113" class="micro muted" text-anchor="middle">NODE</text>
    <text x="615" y="128" class="caption" text-anchor="middle">CHECK</text>
    <path d="M662 116H711" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="728" y="82" width="135" height="68" rx="2" fill="${C.ink}"/>
    <text x="795.5" y="108" class="micro white" text-anchor="middle">N8N</text>
    <text x="795.5" y="128" class="caption white" text-anchor="middle">LOCAL EDITOR</text>
    <path d="M863 116H912" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="929" y="94" width="131" height="44" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="947" cy="116" r="6" fill="${C.ink}"/>
    <text x="1002" y="113" class="micro muted" text-anchor="middle">LIFECYCLE</text>
    <text x="1002" y="128" class="caption" text-anchor="middle">START · STOP</text>
    <circle cx="711" cy="116" r="3" fill="${C.mark}"/>
    <circle cx="912" cy="116" r="3" fill="${C.mark}"/>
  </g>
`,
  repo: `  <g aria-label="Course repository cloned into operator pack">
    <rect x="548" y="82" width="194" height="68" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <path d="M570 100v32M570 108h27M597 108v24M570 124h14" class="line"/>
    <circle cx="570" cy="98" r="5" fill="${C.mark}"/>
    <circle cx="597" cy="108" r="5" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="584" cy="124" r="5" fill="${C.ink}"/>
    <text x="665" y="108" class="micro muted" text-anchor="middle">COURSE</text>
    <text x="665" y="127" class="caption" text-anchor="middle">REPOSITORY</text>
    <path d="M742 116H816" class="redline" marker-end="url(#arrow-red)"/>
    <path d="M834 91H918L932 105H1065V149H834Z" fill="${C.warm}" stroke="${C.strong}"/>
    <rect x="855" y="111" width="58" height="25" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="923" y="111" width="58" height="25" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="991" y="111" width="55" height="25" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="884" y="127" class="tiny muted" text-anchor="middle">BRIEFS</text>
    <text x="952" y="127" class="tiny muted" text-anchor="middle">LOGS</text>
    <text x="1018.5" y="127" class="tiny muted" text-anchor="middle">SITE</text>
    <text x="949.5" y="103" class="micro muted" text-anchor="middle">OPERATOR PACK</text>
  </g>
`,
  claude: `  <g aria-label="Optional Claude Code rail">
    <path d="M552 116H1059" class="goldline dash"/>
    <rect x="568" y="91" width="166" height="50" rx="2" fill="${C.paper}" stroke="${C.gold}" stroke-dasharray="5 4"/>
    <text x="651" y="111" class="micro gold" text-anchor="middle">DECISION GATE</text>
    <text x="651" y="128" class="caption" text-anchor="middle">NEEDED?</text>
    <path d="M734 116H820" class="goldline dash" marker-end="url(#arrow)"/>
    <rect x="837" y="79" width="220" height="74" rx="2" fill="${C.warm}" stroke="${C.gold}" stroke-width="1.5"/>
    <text x="947" y="104" class="micro gold" text-anchor="middle">ENGINE 03 · OPTIONAL</text>
    <text x="947" y="129" class="title" text-anchor="middle">CLAUDE CODE</text>
    <rect x="1000" y="68" width="70" height="18" rx="2" fill="${C.gold}"/>
    <text x="1035" y="80.5" class="tiny white" text-anchor="middle">OPTIONAL</text>
  </g>
`,
  gate: `  <g aria-label="Health gate with green amber and red statuses">
    <rect x="546" y="79" width="126" height="72" rx="2" fill="${C.ink}"/>
    <circle cx="572" cy="100" r="8" fill="${C.paper}" stroke="${C.paper}"/>
    <circle cx="572" cy="116" r="8" fill="${C.gold}"/>
    <circle cx="572" cy="132" r="8" fill="${C.mark}"/>
    <text x="625" y="104" class="micro white" text-anchor="middle">HEALTH</text>
    <text x="625" y="123" class="caption white" text-anchor="middle">GATE</text>
    <path d="M672 116H771" class="line"/>
    <rect x="771" y="101" width="193" height="30" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <text x="867.5" y="120" class="micro" text-anchor="middle">FOUR FILES TOGETHER</text>
    <path d="M964 116H1031" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="1042" y="94" width="40" height="44" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <path d="M1051 107H1073M1051 116H1073M1051 125H1066" class="hair"/>
    <path d="M542 156H1081" class="hair"/>
    <text x="811" y="160" class="tiny muted" text-anchor="middle">GREEN · AMBER · RED — DECLARE WHAT IS TRUE</text>
  </g>
`,
  repair: `  <g aria-label="Repair loop from error to paste to fix to log">
    <rect x="533" y="93" width="116" height="45" rx="2" fill="${C.paper}" stroke="${C.mark}"/>
    <text x="591" y="112" class="micro red" text-anchor="middle">ERROR</text>
    <text x="591" y="127" class="caption" text-anchor="middle">EXACT TEXT</text>
    <rect x="674" y="93" width="116" height="45" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="732" y="112" class="micro muted" text-anchor="middle">PASTE</text>
    <text x="732" y="127" class="caption" text-anchor="middle">WHOLE OUTPUT</text>
    <rect x="815" y="93" width="116" height="45" rx="2" fill="${C.ink}"/>
    <text x="873" y="112" class="micro white" text-anchor="middle">FIX</text>
    <text x="873" y="127" class="caption white" text-anchor="middle">ONE CHANGE</text>
    <rect x="956" y="93" width="116" height="45" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="1014" y="112" class="micro muted" text-anchor="middle">LOG</text>
    <text x="1014" y="127" class="caption" text-anchor="middle">RESULT</text>
    <path d="M649 116H674M790 116H815M931 116H956" class="redline" marker-end="url(#arrow-red)"/>
    <path d="M1014 93V75H591V93" class="hair" marker-end="url(#arrow)"/>
    <text x="803" y="70" class="tiny red" text-anchor="middle">RETRY FROM A FRESH WINDOW · ESCALATE AT 30 MINUTES</text>
  </g>
`,
  healthRun: `  <g aria-label="Laptop terminal and setup log ready for the health run">
    <rect x="534" y="87" width="153" height="53" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <rect x="543" y="95" width="135" height="35" fill="${C.panel}" stroke="${C.rule}"/>
    <path d="M520 145H701L689 151H532Z" fill="${C.panel}" stroke="${C.strong}"/>
    <text x="610.5" y="117" class="micro muted" text-anchor="middle">THIS LAPTOP</text>
    <path d="M704 116H755" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="772" y="84" width="139" height="61" rx="2" fill="${C.ink}"/>
    <text x="788" y="105" class="body white">PS&gt;</text>
    <rect x="817" y="97" width="7" height="12" fill="${C.paper}"/>
    <text x="841.5" y="132" class="tiny white" text-anchor="middle">FRESH TERMINAL</text>
    <path d="M911 116H954" class="redline" marker-end="url(#arrow-red)"/>
    <path d="M971 78H1050L1065 93V148H971Z" fill="${C.paper}" stroke="${C.strong}"/>
    <path d="M1050 78V93H1065M986 106H1049M986 118H1049M986 130H1034" class="hair"/>
    <text x="1018" y="142" class="tiny muted" text-anchor="middle">SETUP LOG</text>
  </g>
`,
  foundations: `  <g aria-label="Five checked foundation layers">
    <rect x="554" y="78" width="502" height="72" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <path d="M554 92H1056M554 106H1056M554 120H1056M554 134H1056" class="hair"/>
    <rect x="554" y="78" width="10" height="72" fill="${C.mark}"/>
    <text x="582" y="89" class="tiny muted">01 · WIN 11 / AMD64</text>
    <text x="582" y="103" class="tiny muted">02 · GIT / NODE / PYTHON</text>
    <text x="582" y="117" class="tiny muted">03 · GIT BASH PATH</text>
    <text x="582" y="131" class="tiny muted">04 · SCRIPT POLICY</text>
    <text x="582" y="145" class="tiny muted">05 · REAL PYTHON</text>
    <circle cx="1035" cy="85" r="4" fill="${C.mark}"/>
    <circle cx="1035" cy="99" r="4" fill="${C.mark}"/>
    <circle cx="1035" cy="113" r="4" fill="${C.mark}"/>
    <circle cx="1035" cy="127" r="4" fill="${C.mark}"/>
    <circle cx="1035" cy="141" r="4" fill="${C.mark}"/>
    <text x="805" y="160" class="tiny red" text-anchor="middle">FOUNDATION HOLDS BEFORE AGENTS RUN</text>
  </g>
`,
  keyHeadroom: `  <g aria-label="Three saved keys and spend headroom gauge">
    <rect x="544" y="87" width="126" height="52" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="683" y="87" width="126" height="52" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="822" y="87" width="139" height="52" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="565" cy="113" r="7" fill="${C.mark}"/>
    <circle cx="704" cy="113" r="7" fill="${C.mark}"/>
    <circle cx="843" cy="113" r="7" fill="${C.mark}"/>
    <text x="619" y="111" class="micro muted" text-anchor="middle">OPENAI</text>
    <text x="619" y="127" class="tiny muted" text-anchor="middle">SAVED</text>
    <text x="758" y="111" class="micro muted" text-anchor="middle">XAI</text>
    <text x="758" y="127" class="tiny muted" text-anchor="middle">SAVED</text>
    <text x="907" y="111" class="micro muted" text-anchor="middle">ANTHROPIC</text>
    <text x="907" y="127" class="tiny muted" text-anchor="middle">SAVED</text>
    <path d="M982 136A38 38 0 0 1 1057 136" class="line"/>
    <path d="M1019.5 136L1041 105" class="goldline"/>
    <circle cx="1019.5" cy="136" r="3.5" fill="${C.gold}"/>
    <text x="1019.5" y="153" class="tiny gold" text-anchor="middle">HEADROOM</text>
  </g>
`,
  agents: `  <g aria-label="Folder containing regenerated proof files from four agents">
    <path d="M535 84H660L676 99H1068V151H535Z" fill="${C.warm}" stroke="${C.strong}"/>
    <text x="562" y="111" class="micro muted">REGENERATE</text>
    <text x="562" y="129" class="caption">ONE FOLDER</text>
    <rect x="690" y="109" width="80" height="27" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="782" y="109" width="80" height="27" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="874" y="109" width="80" height="27" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="966" y="109" width="80" height="27" fill="${C.paper}" stroke="${C.rule}"/>
    <circle cx="704" cy="122.5" r="4" fill="${C.mark}"/>
    <circle cx="796" cy="122.5" r="4" fill="${C.mark}"/>
    <circle cx="888" cy="122.5" r="4" fill="${C.mark}"/>
    <circle cx="980" cy="122.5" r="4" fill="${C.mark}"/>
    <text x="739" y="126" class="tiny muted" text-anchor="middle">CODEX</text>
    <text x="831" y="126" class="tiny muted" text-anchor="middle">OPEN</text>
    <text x="923" y="126" class="tiny muted" text-anchor="middle">PI</text>
    <text x="1015" y="126" class="tiny muted" text-anchor="middle">GOOSE</text>
    <rect x="1008" y="75" width="60" height="18" rx="2" fill="${C.paper}" stroke="${C.gold}"/>
    <text x="1038" y="87.5" class="tiny gold" text-anchor="middle">CLAUDE*</text>
  </g>
`,
  support: `  <g aria-label="Supporting tool chain of Obsidian n8n and course site">
    <path d="M550 115H1060" class="hair"/>
    <path d="M570 84L625 115 570 146 515 115Z" fill="${C.paper}" stroke="${C.strong}"/>
    <text x="570" y="113" class="micro muted" text-anchor="middle">VAULT</text>
    <text x="570" y="128" class="tiny muted" text-anchor="middle">OPENS</text>
    <path d="M625 115H712" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="729" y="83" width="147" height="64" rx="2" fill="${C.ink}"/>
    <text x="802.5" y="111" class="micro white" text-anchor="middle">N8N</text>
    <text x="802.5" y="130" class="caption white" text-anchor="middle">START · SERVE · STOP</text>
    <path d="M876 115H948" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="965" y="91" width="113" height="48" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="1021.5" y="110" class="micro muted" text-anchor="middle">REPO</text>
    <text x="1021.5" y="128" class="caption" text-anchor="middle">SITE SERVES</text>
  </g>
`,
  ready: `  <g aria-label="Four operator readiness checks">
    <rect x="545" y="78" width="515" height="74" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <path d="M802.5 78V152M545 115H1060" class="hair"/>
    <rect x="545" y="78" width="7" height="74" fill="${C.mark}"/>
    <text x="570" y="99" class="micro muted">OPERATOR PACK</text>
    <text x="570" y="110" class="tiny muted">TEMPLATES PRESENT</text>
    <text x="827" y="99" class="micro muted">TWIN ENGINES</text>
    <text x="827" y="110" class="tiny muted">CODEX + OPENCODE</text>
    <text x="570" y="136" class="micro muted">LEAK PLAN</text>
    <text x="570" y="147" class="tiny muted">REVOKE · REPLACE</text>
    <text x="827" y="136" class="micro muted">SETUP LOG</text>
    <text x="827" y="147" class="tiny muted">REAL FAILURE + FIX</text>
    <circle cx="782" cy="96" r="4" fill="${C.mark}"/>
    <circle cx="1040" cy="96" r="4" fill="${C.mark}"/>
    <circle cx="782" cy="133" r="4" fill="${C.mark}"/>
    <circle cx="1040" cy="133" r="4" fill="${C.mark}"/>
  </g>
`,
  result: `  <g aria-label="Honest green amber or red gate declaration">
    <rect x="535" y="84" width="165" height="64" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
    <circle cx="560" cy="116" r="10" fill="${C.paper}" stroke="${C.strong}"/>
    <text x="628" y="112" class="micro" text-anchor="middle">GREEN</text>
    <text x="628" y="130" class="tiny muted" text-anchor="middle">ALL REQUIRED PROOF</text>
    <rect x="719" y="84" width="165" height="64" rx="2" fill="${C.paper}" stroke="${C.gold}"/>
    <circle cx="744" cy="116" r="10" fill="${C.gold}"/>
    <text x="812" y="112" class="micro gold" text-anchor="middle">AMBER</text>
    <text x="812" y="130" class="tiny muted" text-anchor="middle">WORKAROUND LOGGED</text>
    <rect x="903" y="84" width="165" height="64" rx="2" fill="${C.paper}" stroke="${C.mark}"/>
    <circle cx="928" cy="116" r="10" fill="${C.mark}"/>
    <text x="996" y="112" class="micro red" text-anchor="middle">RED</text>
    <text x="996" y="130" class="tiny muted" text-anchor="middle">RESCUE PLAN NEEDED</text>
    <path d="M535 156H1068" class="hair"/>
    <text x="801.5" y="161" class="tiny muted" text-anchor="middle">DECLARE · RECORD · PACK FOR MONDAY</text>
  </g>
`,
};

const installSections = [
  {
    filename: "install-before-you-begin.svg",
    heading: "Before you begin",
    current: 0,
    stage: "BEFORE YOU BEGIN",
    purpose: "Reserve time, keep a log, and bring the three keys.",
    steps: ["TIME BLOCK", "OPEN SETUP LOG", "CONFIRM 3 KEYS", "SEE THE PATH"],
    metaphor: metaphor.begin,
  },
  {
    filename: "install-00-baseline.svg",
    heading: "0 · Baseline machine",
    current: 1,
    stage: "VERIFY THE MACHINE",
    purpose: "Establish a supported Windows 11 operator baseline.",
    steps: ["WIN 11 · 64-BIT", "CHECK AMD64", "FREE 25+ GB", "CONFIRM INSTALL RIGHTS"],
    metaphor: metaphor.baseline,
  },
  {
    filename: "install-01-terminal.svg",
    heading: "1 · Terminal and PowerShell",
    current: 2,
    stage: "OPEN THE CONTROL SURFACE",
    purpose: "Start clean, identify PowerShell, and allow user scripts.",
    steps: ["OPEN TERMINAL", "CHECK SHELL", "SET REMOTESIGNED"],
    metaphor: metaphor.terminal,
  },
  {
    filename: "install-02-winget.svg",
    heading: "2 · winget, the package manager",
    current: 3,
    stage: "MAKE INSTALLS REPEATABLE",
    purpose: "Verify the package conveyor before loading tools.",
    steps: ["FIND WINGET", "REPAIR IF MISSING", "ACCEPT SOURCE TERMS"],
    metaphor: metaphor.winget,
  },
  {
    filename: "install-03-git.svg",
    heading: "3 · Git for Windows",
    current: 4,
    stage: "PLACE THE VERSION RAIL",
    purpose: "Install Git and expose Git Bash to the toolchain.",
    steps: ["INSTALL GIT", "REOPEN TERMINAL", "VERIFY + FIND BASH"],
    metaphor: metaphor.git,
  },
  {
    filename: "install-04-runtime.svg",
    heading: "4 · Node.js and Python",
    current: 5,
    stage: "STAND UP THE RUNTIMES",
    purpose: "Put Node LTS and real Python on a fresh PATH.",
    steps: ["NODE.JS LTS", "PYTHON", "REOPEN TERMINAL", "VERIFY 3 COMMANDS", "CHECK REAL PYTHON"],
    metaphor: metaphor.runtime,
  },
  {
    filename: "install-05-keys.svg",
    heading: "5 · Your three API keys",
    current: 6,
    stage: "LOAD THREE CREDENTIALS",
    purpose: "Save each provider key at user scope, then re-read them.",
    steps: ["READ KEY GUIDE", "SET OPENAI", "SET XAI", "SET ANTHROPIC", "VERIFY NEW WINDOW"],
    metaphor: metaphor.keys,
  },
  {
    filename: "install-06-smoke.svg",
    heading: "6 · Your smoke folder",
    current: 7,
    stage: "CREATE THE PROOF BAY",
    purpose: "Give every agent one shared folder for visible proof.",
    steps: ["CREATE SMOKE FOLDER", "USE FILES AS PROOF"],
    metaphor: metaphor.smoke,
  },
  {
    filename: "install-07-codex.svg",
    heading: "7 · Codex — your home for the week",
    current: 8,
    stage: "ESTABLISH HOME BASE",
    purpose: "Install, key-lock, sandbox, and prove the primary engine.",
    steps: ["INSTALL + VERIFY", "API-KEY SIGN-IN", "LOCK AUTH", "SET SANDBOX", "WRITE FROM-CODEX", "DESKTOP APP*"],
    metaphor: metaphor.codex,
  },
  {
    filename: "install-08-opencode.svg",
    heading: "8 · OpenCode — your second engine",
    current: 9,
    stage: "BRING UP ENGINE TWO",
    purpose: "Install the cohort-pinned xAI engine and write proof.",
    steps: ["KNOW THE ROLE", "GET COHORT PIN", "INSTALL + REOPEN", "VERIFY XAI", "WRITE PROOF"],
    metaphor: metaphor.opencode,
  },
  {
    filename: "install-09-pi.svg",
    heading: "9 · Pi — the bare loop",
    current: 10,
    stage: "EXPOSE THE BARE LOOP",
    purpose: "Install the minimal agent loop and prove shell reach.",
    steps: ["KNOW THE ROLE", "INSTALL PI", "REOPEN + VERIFY", "WRITE PROOF", "REACH SHELL"],
    metaphor: metaphor.pi,
  },
  {
    filename: "install-10-goose.svg",
    heading: "10 · goose — bounded, repeatable work",
    current: 11,
    stage: "BOUND THE RECIPE",
    purpose: "Configure provider, model, path, and repeatable proof.",
    steps: ["NO WINGET", "KEYRING OFF", "PROVIDER + MODEL", "INSTALL + PATH", "VERIFY", "WRITE PROOF"],
    metaphor: metaphor.goose,
  },
  {
    filename: "install-11-obsidian.svg",
    heading: "11 · Obsidian",
    current: 12,
    stage: "OPEN THE VAULT",
    purpose: "Create the local knowledge vault used in class.",
    steps: ["INSTALL OBSIDIAN", "CREATE + OPEN VAULT"],
    metaphor: metaphor.obsidian,
  },
  {
    filename: "install-12-n8n.svg",
    heading: "12 · n8n",
    current: 13,
    stage: "WIRE THE LOCAL FLOW",
    purpose: "Install a compatible editor and learn its lifecycle.",
    steps: ["CHECK NODE", "INSTALL N8N", "START + OPEN", "CREATE LOCAL OWNER", "STOP CLEANLY"],
    metaphor: metaphor.n8n,
  },
  {
    filename: "install-13-repo.svg",
    heading: "13 · Course repo and operator pack",
    current: 14,
    stage: "LOAD THE OPERATOR PACK",
    purpose: "Clone the course, copy templates, and serve safely.",
    steps: ["CLONE REPO", "COPY TEMPLATES", "SERVE SITE", "PROTECT KEYS"],
    metaphor: metaphor.repo,
  },
  {
    filename: "install-14-claude-optional.svg",
    heading: "14 · Claude Code — optional third engine",
    current: 15,
    stage: "ADD ENGINE THREE — OPTIONAL",
    purpose: "Decide deliberately; install only if it is useful.",
    steps: ["DECIDE", "INSTALL + WRITE PROOF"],
    metaphor: metaphor.claude,
    optional: true,
  },
  {
    filename: "install-15-health-gate.svg",
    heading: "15 · Health check gate",
    current: 16,
    stage: "PASS THE INSTALL GATE",
    purpose: "Re-run proof, declare status, and pack for Monday.",
    steps: ["CONFIRM FOUR FILES", "RUN HEALTH GATE", "PACK FOR MONDAY"],
    metaphor: metaphor.gate,
  },
  {
    filename: "install-when-something-breaks.svg",
    heading: "When something breaks",
    current: -1,
    stage: "RUN THE REPAIR LOOP",
    purpose: "Capture the exact failure, fix the environment, and log it.",
    steps: ["COMMAND MISSING", "SCRIPTS BLOCKED", "AUTH FAILS", "FILE MISSING", "ESCALATE AT 30 MIN"],
    metaphor: metaphor.repair,
    crosscut: true,
  },
];

const healthSections = [
  {
    filename: "health-how-to-run.svg",
    heading: "How to run this gate",
    current: 0,
    stage: "START A CLEAN RUN",
    purpose: "Use the Monday laptop, a fresh terminal, and your setup log.",
    steps: ["THIS LAPTOP", "FRESH TERMINAL", "OPEN SETUP LOG"],
    metaphor: metaphor.healthRun,
  },
  {
    filename: "health-a-foundations.svg",
    heading: "A · Foundations",
    current: 1,
    stage: "PROVE THE FOUNDATION",
    purpose: "Re-test the OS, tools, Bash, policy, and real Python.",
    steps: ["WIN 11 · AMD64", "GIT · NODE · PY", "FIND GIT BASH", "SCRIPT POLICY", "REAL PYTHON"],
    metaphor: metaphor.foundations,
  },
  {
    filename: "health-b-keys.svg",
    heading: "B · Your three keys",
    current: 2,
    stage: "CHECK CREDENTIAL HEADROOM",
    purpose: "Confirm all three keys are saved and have room to spend.",
    steps: ["THREE KEYS SAVED", "SPEND ROOM"],
    metaphor: metaphor.keyHeadroom,
  },
  {
    filename: "health-c-agents.svg",
    heading: "C · Four required agents — files on disk",
    current: 3,
    stage: "REGENERATE FOUR PROOFS",
    purpose: "Make each required agent write again into one folder.",
    steps: ["CLEAR OLD FILES", "CODEX", "OPENCODE", "PI + SHELL", "GOOSE", "SEE FOUR · CLAUDE*"],
    metaphor: metaphor.agents,
  },
  {
    filename: "health-d-support.svg",
    heading: "D · Supporting tools",
    current: 4,
    stage: "PROVE SUPPORTING TOOLS",
    purpose: "Open the vault, cycle n8n, and serve the course site.",
    steps: ["OBSIDIAN VAULT", "N8N START · STOP", "REPO + SITE"],
    metaphor: metaphor.support,
  },
  {
    filename: "health-e-ready.svg",
    heading: "E · Operator readiness",
    current: 5,
    stage: "CONFIRM OPERATOR READINESS",
    purpose: "Show the pack, pair, leak plan, and one real repair.",
    steps: ["TEMPLATES", "NAME TWIN ENGINES", "KEY LEAK PLAN", "LOG FAILURE + FIX"],
    metaphor: metaphor.ready,
  },
  {
    filename: "health-result.svg",
    heading: "Gate result",
    current: 6,
    stage: "DECLARE THE GATE",
    purpose: "Name the honest colour, record the run, and pack.",
    steps: ["DECLARE COLOUR", "RECORD THIS RUN", "PACK FOR MONDAY"],
    metaphor: metaphor.result,
  },
];

for (const section of installSections) {
  section.svgTitle = `Install pre-work: ${section.heading}`;
  fs.writeFileSync(path.join(OUT, section.filename), sectionSvg("install", section));
}

for (const section of healthSections) {
  section.svgTitle = `Health gate: ${section.heading}`;
  fs.writeFileSync(path.join(OUT, section.filename), sectionSvg("health", section));
}

function installOverview() {
  return `${svgOpen("Install pre-work journey overview", 280)}${ribbon("install", 0, { overview: true })}
  <text x="24" y="82" class="micro red">MISSION WORKSTATION · FULL PATH</text>
  <text x="24" y="111" class="title">BUILD THE CHAIR. PROVE THE ENGINES.</text>
  <text x="24" y="132" class="purpose">Foundations first; credentials next; every required agent leaves proof on disk.</text>
  <path d="M24 153H1096" class="hair"/>
  <g aria-label="Five install phases">
    <rect x="24" y="166" width="194" height="40" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <rect x="24" y="166" width="7" height="40" fill="${C.mark}"/>
    <text x="42" y="182" class="micro muted">01 · FOUNDATION</text>
    <text x="42" y="197" class="tiny muted">BYB → RUNTIMES</text>
    <path d="M218 186H240" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="250" y="166" width="148" height="40" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="268" y="182" class="micro muted">02 · KEYS</text>
    <text x="268" y="197" class="tiny muted">THREE PROVIDERS</text>
    <path d="M398 186H420" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="430" y="166" width="244" height="40" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="448" y="182" class="micro muted">03 · AGENTS + TOOLS</text>
    <text x="448" y="197" class="tiny muted">SMOKE → N8N</text>
    <path d="M674 186H696" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="706" y="166" width="188" height="40" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="724" y="182" class="micro muted">04 · COURSE KIT</text>
    <text x="724" y="197" class="tiny muted">REPO · CLAUDE*</text>
    <path d="M894 186H916" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="926" y="166" width="170" height="40" rx="2" fill="${C.ink}"/>
    <text x="944" y="182" class="micro white">05 · HEALTH GATE</text>
    <text x="944" y="197" class="tiny white">DECLARE WHAT IS TRUE</text>
  </g>
  <rect x="0" y="220" width="1120" height="60" fill="${C.warm}"/>
  <rect x="24" y="232" width="515" height="36" rx="2" fill="${C.paper}" stroke="${C.strong}"/>
  <circle cx="48" cy="250" r="7" fill="${C.ink}"/>
  <text x="68" y="247" class="micro muted">TWIN-ENGINE READY</text>
  <text x="68" y="260" class="caption">CODEX · OPENCODE</text>
  <rect x="557" y="232" width="539" height="36" rx="2" fill="${C.paper}" stroke="${C.mark}" stroke-width="1.5"/>
  <circle cx="581" cy="250" r="7" fill="${C.mark}"/>
  <path d="M577 250l3 3 6-7" fill="none" stroke="${C.paper}" stroke-width="1.4"/>
  <text x="603" y="247" class="micro red">GREEN · FOUR FILES</text>
  <text x="603" y="260" class="caption">FROM-CODEX · FROM-OPENCODE · FROM-PI · FROM-GOOSE</text>
</svg>
`;
}

function healthOverview() {
  return `${svgOpen("Health gate journey overview", 240)}${ribbon("health", 0, { overview: true })}
  <text x="24" y="80" class="micro red">THIRTY-MINUTE TRUTH TEST</text>
  <text x="24" y="107" class="title">RE-RUN THE MACHINE. DECLARE THE RESULT.</text>
  <text x="24" y="127" class="purpose">Fresh terminal in; verified foundations, keys, four agent files, and support tools out.</text>
  <path d="M24 145H1096" class="hair"/>
  <g aria-label="Health gate flow">
    <rect x="24" y="158" width="151" height="34" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="99.5" y="172" class="tiny muted" text-anchor="middle">FRESH RUN</text>
    <text x="99.5" y="185" class="caption" text-anchor="middle">LAPTOP + LOG</text>
    <path d="M175 175H208" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="218" y="158" width="151" height="34" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="293.5" y="172" class="tiny muted" text-anchor="middle">FOUNDATIONS</text>
    <text x="293.5" y="185" class="caption" text-anchor="middle">TOOLS ANSWER</text>
    <path d="M369 175H402" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="412" y="158" width="151" height="34" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="487.5" y="172" class="tiny muted" text-anchor="middle">CREDENTIALS</text>
    <text x="487.5" y="185" class="caption" text-anchor="middle">3 KEYS FUNDED</text>
    <path d="M563 175H596" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="606" y="151" width="181" height="48" rx="2" fill="${C.ink}"/>
    <text x="696.5" y="170" class="micro white" text-anchor="middle">FOUR AGENT FILES</text>
    <text x="696.5" y="187" class="caption white" text-anchor="middle">REGENERATED TOGETHER</text>
    <path d="M787 175H820" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="830" y="158" width="124" height="34" rx="2" fill="${C.paper}" stroke="${C.rule}"/>
    <text x="892" y="172" class="tiny muted" text-anchor="middle">SUPPORT</text>
    <text x="892" y="185" class="caption" text-anchor="middle">TOOLS READY</text>
    <path d="M954 175H987" class="redline" marker-end="url(#arrow-red)"/>
    <rect x="997" y="151" width="99" height="48" rx="2" fill="${C.paper}" stroke="${C.mark}"/>
    <text x="1046.5" y="170" class="micro red" text-anchor="middle">RESULT</text>
    <text x="1046.5" y="187" class="caption" text-anchor="middle">HONEST</text>
  </g>
  <rect x="0" y="213" width="1120" height="27" fill="${C.warm}"/>
  <circle cx="401" cy="226.5" r="5" fill="${C.paper}" stroke="${C.strong}"/>
  <text x="415" y="230" class="tiny">GREEN</text>
  <circle cx="516" cy="226.5" r="5" fill="${C.gold}"/>
  <text x="530" y="230" class="tiny gold">AMBER</text>
  <circle cx="634" cy="226.5" r="5" fill="${C.mark}"/>
  <text x="648" y="230" class="tiny red">RED</text>
  <text x="765" y="230" class="tiny muted">RECORD THE RUN · PACK FOR MONDAY</text>
</svg>
`;
}

fs.writeFileSync(path.join(OUT, "install-overview.svg"), installOverview());
fs.writeFileSync(path.join(OUT, "health-overview.svg"), healthOverview());

const allFiles = [
  ["install-overview.svg", "Install journey overview for the pre-work hub"],
  ...installSections.map((section) => [section.filename, section.heading]),
  ["health-overview.svg", "Health-gate journey overview"],
  ...healthSections.map((section) => [section.filename, section.heading]),
];

const readme = `# Pre-work section diagrams

Crisp, script-free SVG diagrams for the AI Harness Bootcamp install and health-check pages. All diagrams use the paper-surface Starzl visual system, selectable text, and an internal \`<title>\` for standalone accessibility.

## Asset index

| File | Placement |
|---|---|
${allFiles.map(([file, placement]) => `| \`${file}\` | ${placement} |`).join("\n")}

## Usage

Place the matching figure immediately after its section \`<h2>\`:

\`\`\`html
<figure class="section-diagram">
  <img src="../assets/prework/install-03-git.svg" alt="Diagram: 3 · Git for Windows — place in pre-work journey" width="1120" height="220" loading="lazy" decoding="async" />
</figure>
\`\`\`

Use \`install-overview.svg\` at 1120 × 280 and \`health-overview.svg\` at 1120 × 240. Section diagrams are 1120 × 220. Keep the surrounding figure border in CSS; the SVGs deliberately carry no outer border so they remain reusable in print and other paper surfaces.

Claude Code is encoded with the gold optional treatment. Completed stages use a crimson disc; the current stage uses a filled crimson capsule. The repair diagram is intentionally marked “ANY STAGE” because recovery is cross-cutting rather than a numbered install stage.
`;

fs.writeFileSync(path.join(OUT, "README.md"), readme);

const installRows = installSections
  .map((section) => `| \`${section.heading}\` | \`${section.filename}\` |`)
  .join("\n");
const healthRows = healthSections
  .map((section) => `| \`${section.heading}\` | \`${section.filename}\` |`)
  .join("\n");

const integrate = `# Pre-work diagram integration

The live site files are already integrated. This is the exact insertion pattern for future rebuilds.

## Section snippet

Insert immediately after the matching \`<h2>\`:

\`\`\`html
<figure class="section-diagram">
  <img src="../assets/prework/FILE.svg" alt="Diagram: SECTION TITLE — place in pre-work journey" width="1120" height="220" loading="lazy" decoding="async" />
</figure>
\`\`\`

For the pre-work hub, the overview path is \`./assets/prework/install-overview.svg\`, width 1120, height 280. For the health-check overview, use \`../assets/prework/health-overview.svg\`, width 1120, height 240.

## Install heading map

| Heading | File |
|---|---|
${installRows}

## Health heading map

| Heading | File |
|---|---|
${healthRows}

## CSS

\`\`\`css
.section-diagram {
  margin: 0.35rem 0 1.1rem;
  border: 1px solid var(--rule);
  background: var(--paper-warm);
  overflow: hidden;
}
.section-diagram img,
.section-diagram object,
.section-diagram svg {
  display: block;
  width: 100%;
  height: auto;
  vertical-align: middle;
}
.section-diagram figcaption {
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-faint);
  padding: 0.35rem 0.65rem 0.45rem;
  border-top: 1px solid var(--rule);
}
\`\`\`
`;

fs.writeFileSync(path.join(TMP, "INTEGRATE.md"), integrate);

function figureHtml(src, alt, height) {
  return `<figure class="section-diagram">
  <img src="${src}" alt="Diagram: ${esc(alt)} — place in pre-work journey" width="1120" height="${height}" loading="lazy" decoding="async" />
</figure>`;
}

function integrateSections(file, sections) {
  let html = fs.readFileSync(file, "utf8");
  for (const section of sections) {
    const heading = `<h2>${section.heading}</h2>`;
    const figure = figureHtml(`../assets/prework/${section.filename}`, section.heading, 220);
    if (html.includes(`${heading}${figure}`) || html.includes(`${heading}\n${figure}`)) continue;
    const occurrences = html.split(heading).length - 1;
    if (occurrences !== 1) {
      throw new Error(`Expected one heading in ${file}: ${section.heading}; found ${occurrences}`);
    }
    html = html.replace(heading, `${heading}\n${figure}`);
  }
  html = html.replaceAll("</figure><ol", "</figure>\n<ol");
  fs.writeFileSync(file, html);
}

integrateSections(path.join(ROOT, "site/checklists/prework-install.html"), installSections);
integrateSections(path.join(ROOT, "site/checklists/prework-health.html"), healthSections);

function insertAfterOnce(file, needle, insertion, sentinel) {
  let html = fs.readFileSync(file, "utf8");
  if (html.includes(sentinel)) return;
  const occurrences = html.split(needle).length - 1;
  if (occurrences !== 1) {
    throw new Error(`Expected one insertion anchor in ${file}; found ${occurrences}`);
  }
  html = html.replace(needle, `${needle}\n${insertion}`);
  fs.writeFileSync(file, html);
}

insertAfterOnce(
  path.join(ROOT, "site/prework.html"),
  '    <p class="lede">This module gets your Windows laptop ready for the bootcamp. You install the tools yourself — there is no golden image. Plan a focused evening or weekend block (often about 2–4 hours).</p>',
  `    ${figureHtml("./assets/prework/install-overview.svg", "Install pre-work journey overview", 280).replaceAll("\n", "\n    ")}`,
  "install-overview.svg",
);

insertAfterOnce(
  path.join(ROOT, "site/checklists/prework-health.html"),
  "    <p class=\"lede\">This re-tests everything you installed, independently, and ends with you declaring a colour. Allow about thirty minutes. The point isn't to pass — it's to find out now, while there's still time to fix things, rather than on Monday morning.</p>",
  `${figureHtml("../assets/prework/health-overview.svg", "Health gate journey overview", 240)}`,
  "health-overview.svg",
);

const cssFile = path.join(ROOT, "site/css/course.css");
let css = fs.readFileSync(cssFile, "utf8");
if (!css.includes(".section-diagram {")) {
  css = `${css.trimEnd()}

.section-diagram {
  margin: 0.35rem 0 1.1rem;
  border: 1px solid var(--rule);
  background: var(--paper-warm);
  overflow: hidden;
}
.section-diagram img,
.section-diagram object,
.section-diagram svg {
  display: block;
  width: 100%;
  height: auto;
  vertical-align: middle;
}
.section-diagram figcaption {
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-faint);
  padding: 0.35rem 0.65rem 0.45rem;
  border-top: 1px solid var(--rule);
}
`;
  fs.writeFileSync(cssFile, css);
}

console.log(`Generated ${allFiles.length} SVG assets, README.md, INTEGRATE.md, and site integration.`);
