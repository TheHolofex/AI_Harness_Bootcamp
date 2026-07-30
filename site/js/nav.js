/**
 * Single primary navigation for the whole course site.
 * Depth is inferred from the path so links stay correct from /, /blocks/, /checklists/.
 */
(function () {
  function depthPrefix() {
    var path = (location.pathname || "").replace(/\\/g, "/");
    if (path.indexOf("/blocks/") !== -1 || path.indexOf("/checklists/") !== -1) {
      return "..";
    }
    // site root pages (index, week, prework, …)
    if (path.indexOf("/site/") !== -1 || /\/site$/.test(path.replace(/\/$/, ""))) {
      return ".";
    }
    // file:// or odd hosts: prefer relative from known script location
    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].src || "";
      if (src.indexOf("/js/nav.js") !== -1) {
        if (src.indexOf("/blocks/") !== -1 || src.indexOf("/checklists/") !== -1) return "../..";
        // script is site/js/nav.js → pages in site/ use .
        return ".";
      }
    }
    return ".";
  }

  function pageKey() {
    var path = (location.pathname || "").replace(/\\/g, "/");
    var file = path.split("/").pop() || "index.html";
    if (!file || file === "site") file = "index.html";
    if (path.indexOf("/checklists/") !== -1) {
      if (file === "index.html") return "checklists-index";
      if (file.indexOf("prework-install") === 0) return "prework-install";
      if (file.indexOf("prework-health") === 0) return "prework-health";
      return "checklist-" + file.replace(".html", "");
    }
    if (path.indexOf("/blocks/") !== -1) {
      return "block-" + file.replace(".html", "");
    }
    return file.replace(".html", "") || "index";
  }

  function link(href, label, key, current, extraClass) {
    var cur = key && key === current ? ' aria-current="page"' : "";
    var cls = extraClass ? ' class="' + extraClass + '"' : "";
    return '<a href="' + href + '"' + cls + cur + ">" + label + "</a>";
  }

  function buildNav(prefix, current) {
    var p = prefix;
    var modules = [
["block-b0", p + "/blocks/b0.html", "B0 · Clinic + First Light"],
      ["block-p1", p + "/blocks/p1.html", "P1 · Daily Status Brief"],
      ["block-p2", p + "/blocks/p2.html", "P2 · Hot-rod"],
      ["block-p3", p + "/blocks/p3.html", "P3 · Twin-engine"],
      ["block-p4", p + "/blocks/p4.html", "P4 · Second brain"],
      ["block-p5", p + "/blocks/p5.html", "P5 · Poisoned corpus"],
      ["block-p6", p + "/blocks/p6.html", "P6 · Watch officer"],
      ["block-p7", p + "/blocks/p7.html", "P7 · Automation line"],
      ["block-p8", p + "/blocks/p8.html", "P8 · Open model"],
      ["week", p + "/week.html", "Week map"],
      ["checklists-index", p + "/checklists/index.html", "Exercise checklists"]
    ];
var prework = [
      ["prework", p + "/prework.html", "Pre-work hub"],
      ["keys", p + "/keys.html", "Your API keys"],
      ["prework-install", p + "/checklists/prework-install.html", "Install + verify"],
      ["block-b0", p + "/blocks/b0.html", "Monday clinic + First Light"]
    ];
    var instructor = [
      ["lead", p + "/lead.html", "Operate-along guide"],
      ["pulse", p + "/pulse.html", "Pulse & threads"],
      ["operator", p + "/operator.html", "Operator pack"],
      ["instruments", p + "/instruments.html", "Course instruments"]
    ];

    // Repo-root docs: one level above site/ from root pages, two from blocks/checklists
    var root = p === ".." ? "../.." : "..";
    var resources = [
      ["resources", p + "/resources.html", "Resources hub"],
      ["prompt-direction", p + "/prompt-direction.html", "Prompt & direction tips"],
      ["velocity-paradox", p + "/velocity-paradox.html", "Velocity paradox"],
      ["resources-day", root + "/DAY_PROJECT_TABLE.md", "Day / project table"],
      ["resources-diagrams", root + "/diagrams/README.md", "Diagrams"],
      ["resources-pass", root + "/operator/PASS_BARS.md", "Pass bars"],
      ["resources-measure", root + "/operator/MEASUREMENT_SPINE.md", "Measurement spine"],
      ["resources-transfer", root + "/operator/TRANSFER_30_60_90.md", "Transfer 30-60-90"],
      ["resources-memory", root + "/MEMORY.md", "Project memory"],
      ["resources-start", root + "/START_HERE.md", "START_HERE"]
    ];

    function dropdown(id, label, items, groupKeys) {
      var active = groupKeys.indexOf(current) !== -1;
      var html = '<div class="nav-drop' + (active ? " is-active" : "") + '" data-nav-drop>';
      html += '<button type="button" class="nav-drop-btn"';
      html += ' aria-expanded="false" aria-controls="' + id + '">';
      html += label + '<span class="caret" aria-hidden="true"></span></button>';
      html += '<div class="nav-drop-panel" id="' + id + '" role="group"';
      html += ' aria-label="' + label + ' links">';
      for (var i = 0; i < items.length; i++) {
        var it = items[i];
        html += link(it[1], it[2], it[0], current, "nav-drop-link");
      }
      html += "</div></div>";
      return html;
    }

    var moduleKeys = modules.map(function (m) { return m[0]; });
    var preworkKeys = prework.map(function (m) { return m[0]; });
    var instructorKeys = instructor.map(function (m) { return m[0]; });
    var resourceKeys = resources.map(function (m) { return m[0]; });

    var html = "";
    html += link(p + "/index.html", "Home", "index", current);
    html += dropdown("nav-prework", "Pre-work", prework, preworkKeys);
    html += dropdown("nav-modules", "Modules", modules, moduleKeys);
    html += dropdown("nav-instructor", "Instructor", instructor, instructorKeys);
    html += dropdown("nav-resources", "Resources", resources, resourceKeys);
    return html;
  }

  function wireDropdowns(root) {
    var drops = Array.prototype.slice.call(
      root.querySelectorAll("[data-nav-drop]")
    );

    function buttonFor(drop) {
      return drop.querySelector(".nav-drop-btn");
    }

    function closeDrop(drop) {
      var btn = buttonFor(drop);
      drop.classList.remove("is-open");
      drop.removeAttribute("data-pinned");
      if (btn) btn.setAttribute("aria-expanded", "false");
    }

    function closeAll(except) {
      drops.forEach(function (drop) {
        if (drop !== except) closeDrop(drop);
      });
    }

    function openDrop(drop, pinned) {
      var btn = buttonFor(drop);
      closeAll(drop);
      drop.classList.add("is-open");
      if (pinned) drop.setAttribute("data-pinned", "true");
      if (btn) btn.setAttribute("aria-expanded", "true");
    }

    drops.forEach(function (drop) {
      var btn = buttonFor(drop);
      var panel = drop.querySelector(".nav-drop-panel");
      if (!btn || !panel) return;

      btn.addEventListener("click", function (event) {
        event.stopPropagation();
        var pinned = drop.getAttribute("data-pinned") === "true";
        if (pinned) {
          closeDrop(drop);
        } else {
          openDrop(drop, true);
        }
      });

      btn.addEventListener("keydown", function (event) {
        var links = panel.querySelectorAll("a");
        if (!links.length) return;

        if (event.key === "ArrowDown" || event.key === "ArrowUp") {
          event.preventDefault();
          openDrop(drop, true);
          links[event.key === "ArrowDown" ? 0 : links.length - 1].focus();
        }
      });

      drop.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") return;
        event.preventDefault();
        closeDrop(drop);
        btn.focus();
      });

      drop.addEventListener("mouseenter", function () {
        openDrop(drop, false);
      });

      drop.addEventListener("mouseleave", function () {
        if (
          drop.getAttribute("data-pinned") !== "true" &&
          !drop.contains(document.activeElement)
        ) {
          closeDrop(drop);
        }
      });
    });

    root.addEventListener("focusout", function (event) {
      if (!event.relatedTarget || !root.contains(event.relatedTarget)) closeAll();
    });

    document.addEventListener("click", function () {
      closeAll();
    });
  }

  function init() {
    var nav = document.querySelector("nav.nav, nav#primary-nav");
    if (!nav) return;
    var prefix = depthPrefix();
    // When page is site/checklists/x and script is ../js, prefix .. is correct.
    // When opened as file://.../site/index.html, prefix .
    var current = pageKey();
    nav.setAttribute("aria-label", "Primary");
    nav.classList.add("nav", "nav-unified");
    nav.innerHTML = buildNav(prefix, current);
    wireDropdowns(nav);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
