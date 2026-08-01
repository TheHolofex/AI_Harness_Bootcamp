/**
 * AHB shared shell — one include across every page (after registry.js).
 *
 * Renders the primary nav (day dropdowns with per-block status dots),
 * the block context strip, the prev/next plate, wires checklist forms,
 * and feeds the home dashboard + pre-work hub panels. All progress reads
 * go through the registry in registry.js.
 */
(function () {
  "use strict";

  var AHB = window.AHB;
  if (!AHB) return;

  /* ---------- site root ---------- */

  function siteRootPrefix() {
    var script = document.currentScript || document.querySelector('script[src*="/js/shell.js"], script[src$="js/shell.js"]');
    if (!script || !script.src) return ".";
    return new URL("../", script.src).href.replace(/\/$/, "");
  }

  function pageKey() {
    if (document.body && document.body.getAttribute("data-section") === "resources") return "resources";
    var path = (location.pathname || "").replace(/\\/g, "/");
    var file = path.split("/").pop() || "index.html";
    if (!file || file === "site") file = "index.html";
    if (path.indexOf("/checklists/") !== -1) {
      if (file.indexOf("prework-install") === 0) return "prework-install";
      return "checklist-" + file.replace(".html", "");
    }
    if (path.indexOf("/blocks/") !== -1) return "block-" + file.replace(".html", "");
    return file.replace(".html", "") || "index";
  }

  /* ---------- status helpers ---------- */

  function statusOf(b, current) {
    if (AHB.isComplete(b)) return "done";
    if (current && b.code === current.code) return "current";
    return "ahead";
  }

  function dotHtml(status) {
    var ch = status === "ahead" ? "○" : "●";
    var word = status === "current" ? "you are here" : status;
    return '<span class="nav-dot dot-' + status + '" aria-hidden="true">' + ch + "</span>" +
      '<span class="visually-hidden">' + word + " · </span>";
  }

  function blockLabel(b) {
    return b.slot === "read" || b.slot === "pre" ? b.title : b.code + " · " + b.title;
  }

  function dayLabel(b) {
    return b.slot === "read" || b.slot === "pre" ? b.day : b.day + " " + b.slot;
  }

  /* ---------- primary nav ---------- */

  var RESOURCE_SHELVES = [
    { label: "Resource hub", path: "resources.html" },
    { label: "Pre-work", path: "resources/prework/index.html" },
    { label: "P1 · Daily Status Brief", path: "resources/p1/index.html" },
    { label: "P2 · Hot-rod morning", path: "resources/p2/index.html" },
    { label: "P3 · Twin-engine intel desk", path: "resources/p3/index.html" },
    { label: "P4 · Director’s second brain", path: "resources/p4/index.html" },
    { label: "P5 · Poisoned corpus", path: "resources/p5/index.html" },
    { label: "P6 · Watch officer", path: "resources/p6/index.html" },
    { label: "P7 · Automation line", path: "resources/p7/index.html" },
    { label: "P8 · Operator-governed model", path: "resources/p8/index.html" },
    { label: "Course-wide", path: "resources/course-wide/index.html" }
  ];

  function navGroupFor(current) {
    if (current === "index") return "home";
    if (current === "prework" || current === "keys" || current === "prework-install") return "prework";
    if (current === "resources" || current === "pulse" ||
        current === "prompt-direction" || current === "velocity-paradox") return "resources";
    if (current === "lead" || current === "operator" || current === "instruments") return "lead";
    return "";
  }

  function buildNav(prefix, current) {
    var p = prefix;
    var cur = AHB.currentBlock();
    var group = navGroupFor(current);

    function topLink(href, label, active, quiet) {
      return '<a href="' + href + '"' +
        (quiet ? ' class="nav-quiet"' : "") +
        (active ? ' aria-current="page"' : "") + ">" + label + "</a>";
    }

    var html = "";
    html += topLink(p + "/index.html", "Home", group === "home");
    html += topLink(p + "/prework.html", "Pre-work", group === "prework");

    AHB.DAY_NAV.forEach(function (day, di) {
      var dayActive = day.codes.some(function (c) {
        return current === "block-" + c.toLowerCase();
      });
      html += '<div class="nav-drop' + (dayActive ? " is-active" : "") + '" data-nav-drop>';
      html += '<button type="button" class="nav-drop-btn" aria-expanded="false"' +
        ' aria-controls="nav-day-' + di + '">' + day.label +
        '<span class="caret" aria-hidden="true"></span></button>';
      html += '<div class="nav-drop-panel nav-drop-blocks" id="nav-day-' + di + '"' +
        ' role="group" aria-label="' + day.label + ' blocks">';
      day.codes.forEach(function (code) {
        var b = AHB.block(code);
        var st = statusOf(b, cur);
        var isHere = current === "block-" + code.toLowerCase();
        html += '<a class="nav-drop-item' + (st === "done" ? " is-done" : "") + '"' +
          ' href="' + p + "/" + b.url + '"' + (isHere ? ' aria-current="page"' : "") + ">";
        html += dotHtml(st);
        html += '<span class="nav-drop-name"><strong>' + b.code + "</strong> · " + b.name + "</span>";
        html += '<span class="nav-drop-slot">' + b.slot + "</span>";
        html += "</a>";
      });
      html += "</div></div>";
    });

    html += '<span class="nav-sep" aria-hidden="true"></span>';
    html += '<div class="nav-drop nav-drop-resources' + (group === "resources" ? " is-active" : "") + '" data-nav-drop>';
    html += '<button type="button" class="nav-drop-btn nav-quiet" aria-expanded="false" aria-controls="nav-resources">Resources<span class="caret" aria-hidden="true"></span></button>';
    html += '<div class="nav-drop-panel nav-drop-resource-shelves" id="nav-resources" role="group" aria-label="Resource module shelves" hidden>';
    RESOURCE_SHELVES.forEach(function (shelf) {
      html += '<a class="nav-drop-link" href="' + p + "/" + shelf.path + '">' + shelf.label + '</a>';
    });
    html += "</div></div>";
    html += topLink(p + "/lead.html", "Lead", group === "lead", true);
    return html;
  }

  function wireDropdowns(root) {
    var drops = Array.prototype.slice.call(root.querySelectorAll("[data-nav-drop]"));

    function buttonFor(drop) { return drop.querySelector(".nav-drop-btn"); }

    function closeDrop(drop) {
      var btn = buttonFor(drop);
      var panel = drop.querySelector(".nav-drop-panel");
      drop.classList.remove("is-open");
      drop.removeAttribute("data-pinned");
      if (btn) btn.setAttribute("aria-expanded", "false");
      if (panel) panel.hidden = true;
    }

    function closeAll(except) {
      drops.forEach(function (drop) { if (drop !== except) closeDrop(drop); });
    }

    function openDrop(drop, pinned) {
      var btn = buttonFor(drop);
      var panel = drop.querySelector(".nav-drop-panel");
      closeAll(drop);
      drop.classList.add("is-open");
      if (pinned) drop.setAttribute("data-pinned", "true");
      if (btn) btn.setAttribute("aria-expanded", "true");
      if (panel) panel.hidden = false;
    }

    drops.forEach(function (drop) {
      var btn = buttonFor(drop);
      var panel = drop.querySelector(".nav-drop-panel");
      if (!btn || !panel) return;

      btn.addEventListener("click", function (event) {
        event.stopPropagation();
        if (drop.getAttribute("data-pinned") === "true") closeDrop(drop);
        else openDrop(drop, true);
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

      drop.addEventListener("mouseenter", function () { openDrop(drop, false); });

      drop.addEventListener("mouseleave", function () {
        if (drop.getAttribute("data-pinned") !== "true" &&
            !drop.contains(document.activeElement)) {
          closeDrop(drop);
        }
      });
    });

    root.addEventListener("focusout", function (event) {
      if (!event.relatedTarget || !root.contains(event.relatedTarget)) closeAll();
    });

    document.addEventListener("click", function () { closeAll(); });
  }

  function renderNav() {
    var nav = document.querySelector("nav.nav, nav#primary-nav");
    if (!nav) return;
    nav.setAttribute("aria-label", "Primary");
    nav.classList.add("nav", "nav-unified");
    nav.innerHTML = buildNav(siteRootPrefix(), pageKey());
    wireDropdowns(nav);
  }

  /* ---------- context strip + prev/next plate ---------- */

  function neighbors(code) {
    var i = -1;
    for (var k = 0; k < AHB.REGISTRY.length; k++) {
      if (AHB.REGISTRY[k].code === code) { i = k; break; }
    }
    if (i === -1) return { prev: null, next: null };
    return {
      prev: i > 0 ? AHB.REGISTRY[i - 1] : null,
      next: i < AHB.REGISTRY.length - 1 ? AHB.REGISTRY[i + 1] : null
    };
  }

  function renderContextStrips(prefix) {
    var strips = document.querySelectorAll("[data-context-for]");
    Array.prototype.forEach.call(strips, function (el) {
      var b = AHB.block(el.getAttribute("data-context-for"));
      if (!b) return;
      var nb = neighbors(b.code);
      var label = dayLabel(b) + " · Block " + AHB.blockNumber(b.code) +
        " of " + AHB.TOTAL_BLOCKS;
      var html = '<div class="context-strip-inner">';
      html += nb.prev
        ? '<a class="context-prev" href="' + prefix + "/" + nb.prev.url + '">← ' +
          blockLabel(nb.prev) + "</a>"
        : '<a class="context-prev" href="' + prefix + '/index.html">← Home</a>';
      html += '<span class="context-label">' + label + "</span>";
      html += nb.next
        ? '<a class="context-next" href="' + prefix + "/" + nb.next.url + '">' +
          blockLabel(nb.next) + " →</a>"
        : '<a class="context-next" href="' + prefix + '/index.html#journey">Week map →</a>';
      html += "</div>";
      el.classList.add("context-strip");
      el.innerHTML = html;
    });
  }

  function renderPlates(prefix) {
    var plates = document.querySelectorAll("[data-plate-for]");
    Array.prototype.forEach.call(plates, function (el) {
      var b = AHB.block(el.getAttribute("data-plate-for"));
      if (!b) return;
      var nb = neighbors(b.code);
      var html = "";
      if (nb.prev) {
        html += '<a class="plate-cell" href="' + prefix + "/" + nb.prev.url + '">' +
          '<span class="plate-eyebrow">← Previous · ' + dayLabel(nb.prev) + "</span>" +
          '<span class="plate-title">' + blockLabel(nb.prev) + "</span></a>";
      } else {
        html += '<a class="plate-cell" href="' + prefix + '/index.html">' +
          '<span class="plate-eyebrow">← Start</span>' +
          '<span class="plate-title">Home</span></a>';
      }
      html += '<a class="plate-mid" href="' + prefix + '/index.html#journey">Week map</a>';
      if (nb.next) {
        html += '<a class="plate-cell plate-next" href="' + prefix + "/" + nb.next.url + '">' +
          '<span class="plate-eyebrow">Next · ' + dayLabel(nb.next) + " →</span>" +
          '<span class="plate-title">' + blockLabel(nb.next) + "</span></a>";
      } else {
        html += '<div class="plate-cell plate-next">' +
          '<span class="plate-eyebrow">After Friday</span>' +
          '<span class="plate-title">Transfer 30-60-90 · your own desk</span></div>';
      }
      el.classList.add("plate");
      el.innerHTML = html;
    });
  }

  /* ---------- checklist forms ---------- */

  function isOptional(id) {
    return typeof id === "string" && id.indexOf("stretch-") === 0;
  }

  function saveState(key, state) {
    try { localStorage.setItem(key, JSON.stringify(state)); }
    catch (e) { /* private mode: checks still work for the session */ }
  }

  function progressText(b) {
    var done = AHB.countDone(b);
    var total = b.ids.length || 1;
    var pct = Math.round((done / total) * 100);
    var text = done + " / " + total + " · " + pct + "%";
    if (b.stretchIds.length) {
      text += " · " + (b.optionalLabel || "stretch") + " " +
        AHB.countStretchDone(b) + "/" + b.stretchIds.length;
    }
    return { text: text, pct: pct };
  }

  function updateProgressOutputs(key) {
    var b = null;
    for (var i = 0; i < AHB.REGISTRY.length; i++) {
      if (AHB.REGISTRY[i].key === key) { b = AHB.REGISTRY[i]; break; }
    }
    if (!b) return;
    var p = progressText(b);
    var lines = document.querySelectorAll('[data-progress-for="' + key + '"]');
    Array.prototype.forEach.call(lines, function (el) {
      el.textContent = el.getAttribute("data-progress-format") === "pct"
        ? p.pct + "%"
        : p.text;
    });
    var bars = document.querySelectorAll('[data-progress-bar-for="' + key + '"]');
    Array.prototype.forEach.call(bars, function (el) { el.style.width = p.pct + "%"; });

    var sections = document.querySelectorAll("[data-check-section]");
    Array.prototype.forEach.call(sections, function (section) {
      var name = section.getAttribute("data-check-section");
      var boxes = section.querySelectorAll('input[type="checkbox"][data-check-id]');
      var total = 0, done = 0;
      Array.prototype.forEach.call(boxes, function (box) {
        if (isOptional(box.getAttribute("data-check-id"))) return;
        total++;
        if (box.checked) done++;
      });
      var counts = document.querySelectorAll('[data-count-for="' + name + '"]');
      Array.prototype.forEach.call(counts, function (el) {
        el.textContent = done + "/" + total;
      });
    });
  }

  function applyItemState(input) {
    var li = input.closest("[data-check-item]");
    if (li) li.classList.toggle("is-done", input.checked);
  }

  function initForm(form) {
    var key = form.getAttribute("data-storage-key");
    if (!key) return;
    var state = AHB.readState(key);
    var boxes = form.querySelectorAll('input[type="checkbox"][data-check-id]');
    Array.prototype.forEach.call(boxes, function (input) {
      var id = input.getAttribute("data-check-id");
      input.checked = !!state[id];
      applyItemState(input);
      input.addEventListener("change", function () {
        var s = AHB.readState(key);
        s[id] = input.checked;
        s._updated = new Date().toISOString();
        saveState(key, s);
        applyItemState(input);
        updateProgressOutputs(key);
      });
    });
    updateProgressOutputs(key);
  }

  function wireChecklistTools() {
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-checklist-reset]"),
      function (btn) {
        btn.addEventListener("click", function () {
          var key = btn.getAttribute("data-storage-key");
          if (!key) return;
          if (!confirm("Reset all checks for this block on this browser?")) return;
          localStorage.removeItem(key);
          var form = document.querySelector('form[data-storage-key="' + key + '"]');
          if (!form) return location.reload();
          var boxes = form.querySelectorAll('input[type="checkbox"][data-check-id]');
          Array.prototype.forEach.call(boxes, function (input) {
            input.checked = false;
            applyItemState(input);
          });
          updateProgressOutputs(key);
        });
      }
    );
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-checklist-expand]"),
      function (btn) {
        btn.addEventListener("click", function () {
          Array.prototype.forEach.call(
            document.querySelectorAll(".check-detail"),
            function (el) { el.style.display = ""; }
          );
        });
      }
    );
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-checklist-collapse]"),
      function (btn) {
        btn.addEventListener("click", function () {
          Array.prototype.forEach.call(
            document.querySelectorAll(".check-detail"),
            function (el) { el.style.display = "none"; }
          );
        });
      }
    );
  }

  /* ---------- home dashboard ---------- */

  function setText(sel, text) {
    var el = document.querySelector(sel);
    if (el) el.textContent = text;
  }

  function renderDashboard(prefix) {
    var board = document.querySelector("[data-journey]");
    var panel = document.querySelector("[data-yah-title]");
    if (!board && !panel) return;

    var cur = AHB.currentBlock();

    if (panel) {
      var done = AHB.countDone(cur);
      var total = cur.ids.length || 1;
      var pct = Math.round((done / total) * 100);
      setText("[data-yah-eyebrow]", cur.slot === "pre"
        ? "Before Monday · Pre-work"
        : dayLabel(cur) + " · " + cur.code);
      setText("[data-yah-title]", cur.title);
      setText("[data-yah-line]", done + " / " + total + " steps · " + pct + "%");
      var bar = document.querySelector("[data-yah-bar]");
      if (bar) bar.style.width = pct + "%";
      var cta = document.querySelector("[data-yah-cta]");
      if (cta) {
        cta.textContent = done > 0 ? "Continue where you left off" : "Start this block";
        cta.setAttribute("href", prefix + "/" + cur.url);
      }
    }

    if (board) {
      var html = "";
      AHB.JOURNEY.forEach(function (col) {
        var hasCurrent = col.codes.indexOf(cur.code) !== -1;
        html += '<div class="journey-col">';
        html += '<div class="journey-head' + (hasCurrent ? " is-current" : "") + '">';
        html += '<p class="journey-phase">' + col.phase + "</p>";
        html += '<p class="journey-title">' + col.title + "</p>";
        html += "</div>";
        html += '<div class="journey-cells">';
        col.codes.forEach(function (code) {
          var b = AHB.block(code);
          var st = statusOf(b, cur);
          var meta = b.slot === "read" || b.slot === "pre" ? b.meta : b.slot + " · " + b.meta;
          html += '<a class="journey-cell is-' + st + '"' +
            (st === "current" ? ' aria-current="step"' : "") +
            ' href="' + prefix + "/" + b.url + '">';
          html += dotHtml(st);
          html += "<span>";
          html += '<span class="journey-name">' + b.code + " · " + b.name + "</span>";
          html += '<span class="journey-meta">' + meta + "</span>";
          html += "</span></a>";
        });
        html += "</div></div>";
      });
      board.innerHTML = html;
    }

    var install = AHB.block("INSTALL");
    var stat = document.querySelector("[data-prework-stat]");
    if (stat && install) {
      var idone = AHB.countDone(install);
      stat.textContent = idone + " / " + install.ids.length + " steps checked";
      stat.classList.toggle("is-done", idone >= install.ids.length);
    }
  }

  /* ---------- pre-work hub ---------- */

  function renderPreworkHub(prefix) {
    var hub = document.querySelector("[data-prework-hub]");
    if (!hub) return;

    var install = AHB.block("INSTALL");
    var done = AHB.countDone(install);
    var total = install.ids.length;
    var pct = Math.round((done / total) * 100);
    var complete = done >= total;
    var started = done > 0;
    // Reading the keys page precedes checklist work on the student path.
    var keysRead = started;

    setText("[data-hub-headline]", complete
      ? "Pre-work complete — see you Monday"
      : started ? "Install in progress" : "Not started yet");
    setText("[data-hub-line]", done + " / " + total + " install steps · " + pct + "%");
    var bar = document.querySelector("[data-hub-bar]");
    if (bar) bar.style.width = pct + "%";
    var cta = document.querySelector("[data-hub-cta]");
    if (cta) {
      if (complete) {
        cta.textContent = "Review the checklist";
        cta.setAttribute("href", prefix + "/checklists/prework-install.html");
      } else if (started) {
        cta.textContent = "Continue the install checklist";
        cta.setAttribute("href", prefix + "/checklists/prework-install.html");
      } else {
        cta.textContent = "Start with Your API keys";
        cta.setAttribute("href", prefix + "/keys.html");
      }
    }

    function setStage(name, state, statText, statClass) {
      var card = document.querySelector('[data-stage="' + name + '"]');
      if (!card) return;
      card.classList.remove("is-done", "is-current");
      if (state) card.classList.add(state);
      var stat = card.querySelector("[data-stage-stat]");
      if (stat) {
        stat.textContent = statText;
        stat.classList.remove("stat-done", "stat-current");
        if (statClass) stat.classList.add(statClass);
      }
    }

    setStage("keys",
      keysRead ? "is-done" : null,
      keysRead ? "Read" : "Not read yet",
      keysRead ? "stat-done" : null);
    setStage("install",
      complete ? "is-done" : started ? "is-current" : null,
      done + " / " + total + " steps checked",
      complete ? "stat-done" : started ? "stat-current" : null);
    setStage("monday", null, "Opens Monday", null);
  }

  /* ---------- copy buttons on code blocks ---------- */

  function copyFallback(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function wireCopyButtons() {
    var pres = document.querySelectorAll(".site-main pre");
    Array.prototype.forEach.call(pres, function (pre) {
      var code = pre.querySelector("code");
      if (!code || pre.querySelector(".copy-btn")) return;
      pre.classList.add("has-copy");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy this block to the clipboard");
      btn.addEventListener("click", function () {
        var text = code.textContent.replace(/\s+$/, "");
        function flash(ok) {
          btn.textContent = ok ? "Copied ✓" : "Press Ctrl+C";
          btn.classList.add("copied");
          window.setTimeout(function () {
            btn.textContent = "Copy";
            btn.classList.remove("copied");
          }, 1600);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(
            function () { flash(true); },
            function () { flash(copyFallback(text)); }
          );
        } else {
          flash(copyFallback(text));
        }
      });
      pre.appendChild(btn);
    });
  }

  /* ---------- boot ---------- */

  function init() {
    var prefix = siteRootPrefix();
    renderNav();
    renderContextStrips(prefix);
    renderPlates(prefix);
    Array.prototype.forEach.call(
      document.querySelectorAll("form[data-checklist]"),
      initForm
    );
    wireChecklistTools();
    renderDashboard(prefix);
    renderPreworkHub(prefix);
    wireCopyButtons();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
