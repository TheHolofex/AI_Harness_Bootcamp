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

  function pageOwnerCode(current) {
    if (current === "prework-install") return "B0";
    if (current === "prework" || current === "keys" ||
        current === "prework-setup-log") return "PREWORK";
    if (current.indexOf("block-") === 0) return current.replace("block-", "").toUpperCase();
    var module = document.body && document.body.getAttribute("data-module");
    if (module === "prework") return "PREWORK";
    if (module && /^p[1-8]$/.test(module)) return module.toUpperCase();
    return "";
  }

  function buildNav(prefix, current) {
    var p = prefix;
    var cur = AHB.currentBlock();
    var owner = pageOwnerCode(current);

    function topLink(href, label, active) {
      return '<a href="' + href + '"' +
        (active ? ' aria-current="page"' : "") + ">" + label + "</a>";
    }

    var html = "";
    html += topLink(p + "/prework.html", "Pre-work", owner === "PREWORK");

    AHB.DAY_NAV.forEach(function (day, di) {
      var dayActive = day.codes.indexOf(owner) !== -1;
      html += '<div class="nav-drop' + (dayActive ? " is-active" : "") + '" data-nav-drop>';
      html += '<button type="button" class="nav-drop-btn" aria-expanded="false"' +
        ' aria-controls="nav-day-' + di + '"><span class="nav-day-name">' + day.label + "</span>" +
        '<span class="caret" aria-hidden="true"></span></button>';
      html += '<div class="nav-drop-panel nav-drop-blocks" id="nav-day-' + di + '"' +
        ' role="group" aria-label="' + day.label + ' modules" hidden>';
      day.codes.forEach(function (code) {
        var b = AHB.block(code);
        var st = statusOf(b, cur);
        var isHere = owner === code;
        html += '<a class="nav-drop-item' + (st === "done" ? " is-done" : "") + '"' +
          ' href="' + p + "/" + b.url + '"' + (isHere ? ' aria-current="page"' : "") + ">";
        html += dotHtml(st);
        html += '<span class="nav-drop-name"><strong>' + b.code + "</strong> · " + b.name + "</span>";
        html += '<span class="nav-drop-slot">' + b.slot + "</span>";
        html += "</a>";
      });
      html += "</div></div>";
    });
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
    for (var k = 0; k < AHB.CORE_PATH.length; k++) {
      if (AHB.CORE_PATH[k].code === code) { i = k; break; }
    }
    if (i === -1) return { prev: null, next: null };
    return {
      prev: i > 0 ? AHB.CORE_PATH[i - 1] : null,
      next: i < AHB.CORE_PATH.length - 1 ? AHB.CORE_PATH[i + 1] : null
    };
  }

  function renderContextStrips(prefix) {
    var strips = document.querySelectorAll("[data-context-for]");
    Array.prototype.forEach.call(strips, function (el) {
      var b = AHB.block(el.getAttribute("data-context-for"));
      if (!b) return;
      var nb = neighbors(b.code);
      var label = b.kind === "install"
        ? "Monday AM · B0 · Pre-work Install Clinic"
        : dayLabel(b) + " · Module " + AHB.moduleNumber(b.code) +
          " of " + AHB.TOTAL_MODULES;
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

  function isRequiredId(b, id) {
    return !!b && b.ids.indexOf(id) !== -1;
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
        if (box.closest("[data-check-section]") !== section) return;
        if (!isRequiredId(b, box.getAttribute("data-check-id"))) return;
        total++;
        if (box.checked) done++;
      });
      var counts = document.querySelectorAll('[data-count-for="' + name + '"]');
      Array.prototype.forEach.call(counts, function (el) {
        el.textContent = done + "/" + total;
      });
    });

    if (key === "ahb-prework-install") {
      var prework = AHB.preworkProgress();
      Array.prototype.forEach.call(document.querySelectorAll("[data-phase-stat]"), function (el) {
        var id = el.getAttribute("data-phase-stat");
        var phase = prework.phases.filter(function (item) { return item.id === id; })[0];
        if (!phase) return;
        var currentPhase = !phase.complete && prework.firstPhase && prework.firstPhase.id === phase.id;
        el.textContent = phase.complete
          ? "✓ Complete"
          : (currentPhase ? "Current · " : "") + phase.done + " / " + phase.total;
        el.classList.toggle("is-done", phase.complete);
        el.classList.toggle("is-current", currentPhase);
        var link = el.closest("a");
        if (link) {
          link.classList.toggle("is-done", phase.complete);
          link.classList.toggle("is-current", currentPhase);
          if (currentPhase) link.setAttribute("aria-current", "step");
          else link.removeAttribute("aria-current");
        }
      });
      var preworkForm = document.querySelector('form[data-storage-key="ahb-prework-install"]');
      if (preworkForm) updatePreworkSectionStatuses(preworkForm, b);
    }
  }

  function applyItemState(input) {
    var li = input.closest("[data-check-item]");
    if (li) li.classList.toggle("is-done", input.checked);
  }

  function setPreworkSection(section, open) {
    if (!section) return;
    section.classList.toggle("is-section-collapsed", !open);
    var button = section.querySelector("[data-phase-section-toggle]");
    if (button) button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function updatePreworkSectionStatuses(form, b) {
    if (!form || !b || b.code !== "INSTALL") return;
    var sections = form.querySelectorAll("[data-phase-section]");
    var currentSection = null;
    Array.prototype.forEach.call(sections, function (section) {
      var boxes = section.querySelectorAll('input[type="checkbox"][data-check-id]');
      var done = 0, total = 0;
      Array.prototype.forEach.call(boxes, function (box) {
        if (!isRequiredId(b, box.getAttribute("data-check-id"))) return;
        total++;
        if (box.checked) done++;
      });
      var complete = total > 0 && done === total;
      if (!complete && !currentSection) currentSection = section;
      section.classList.toggle("is-section-done", complete);
      section.classList.remove("is-section-current");
      var stat = section.querySelector("[data-phase-section-stat]");
      if (stat) stat.textContent = complete ? "✓ Complete" : done + " / " + total;
    });
    if (currentSection) {
      currentSection.classList.add("is-section-current");
      var currentStat = currentSection.querySelector("[data-phase-section-stat]");
      if (currentStat) currentStat.textContent = "Current · " + currentStat.textContent;
      setPreworkSection(currentSection, true);
    }
  }

  function initPreworkSections(form, b) {
    if (!b || b.code !== "INSTALL") return;
    var sections = form.querySelectorAll(".checklist-section");
    var sectionIndex = 0;
    Array.prototype.forEach.call(sections, function (section) {
      if (section.closest("details.lane-disclosure")) return;
      var heading = section.querySelector("h3");
      var list = section.querySelector("ol.checklist");
      if (!heading || !list) return;
      sectionIndex++;
      section.setAttribute("data-phase-section", "");
      heading.classList.add("phase-section-heading");

      var title = heading.textContent;
      heading.textContent = "";
      var button = document.createElement("button");
      button.type = "button";
      button.className = "phase-section-toggle";
      var buttonId = "prework-section-toggle-" + sectionIndex;
      button.setAttribute("id", buttonId);
      button.setAttribute("data-phase-section-toggle", "");
      button.setAttribute("aria-expanded", "false");

      var label = document.createElement("span");
      label.className = "phase-section-title";
      label.textContent = title;
      var stat = document.createElement("span");
      stat.className = "phase-section-stat";
      stat.setAttribute("data-phase-section-stat", "");
      stat.textContent = "0 / 0";
      var cue = document.createElement("span");
      cue.className = "phase-section-cue";
      cue.setAttribute("aria-hidden", "true");
      button.appendChild(label);
      button.appendChild(stat);
      button.appendChild(cue);
      heading.appendChild(button);

      if (!list.getAttribute("id")) list.setAttribute("id", "prework-section-steps-" + sectionIndex);
      list.setAttribute("aria-labelledby", buttonId);
      button.setAttribute("aria-controls", list.getAttribute("id"));
      setPreworkSection(section, false);
      button.addEventListener("click", function () {
        setPreworkSection(section, button.getAttribute("aria-expanded") !== "true");
      });
    });
  }

  function setCheckDetail(detail, open) {
    if (!detail) return;
    if (open) setPreworkSection(detail.closest("[data-phase-section]"), true);
    detail.hidden = !open;
    var item = detail.closest("[data-check-item]");
    var button = item && item.querySelector("[data-check-detail-toggle]");
    if (button) {
      button.setAttribute("aria-expanded", open ? "true" : "false");
      button.textContent = open ? "Hide instructions ↑" : "Show instructions ↓";
    }
  }

  function initPreworkStepDetails(form, b) {
    if (!b || b.code !== "INSTALL") return;
    var items = form.querySelectorAll("[data-check-item]");
    Array.prototype.forEach.call(items, function (item, index) {
      var detail = item.querySelector(".check-detail");
      var label = item.querySelector(".check-label");
      if (!detail || !label) return;
      if (!detail.id) detail.id = "prework-step-detail-" + (index + 1);
      var button = document.createElement("button");
      button.type = "button";
      button.className = "check-detail-toggle";
      button.setAttribute("data-check-detail-toggle", "");
      button.setAttribute("aria-controls", detail.id);
      button.setAttribute("aria-expanded", "false");
      button.textContent = "Show instructions ↓";
      label.insertAdjacentElement("afterend", button);
      setCheckDetail(detail, false);
      button.addEventListener("click", function () {
        setCheckDetail(detail, button.getAttribute("aria-expanded") !== "true");
      });
    });

    function openHashTarget(rawHash) {
      var hash = "";
      try { hash = decodeURIComponent((rawHash || "").replace(/^#/, "")); }
      catch (e) { hash = (rawHash || "").replace(/^#/, ""); }
      var target = hash ? document.getElementById(hash) : null;
      var targetItem = target && target.closest ? target.closest("[data-check-item]") : null;
      var phaseTarget = target && target.matches && target.matches('section[id^="phase-"]');
      var boxes = form.querySelectorAll('input[type="checkbox"][data-check-id]');

      // A visual phase spans several sibling tool sections. Use the registry's
      // phase membership rather than only searching the section with the anchor.
      if (!targetItem && phaseTarget) {
        var phase = null;
        for (var p = 0; p < AHB.PREWORK_PHASES.length; p++) {
          if (AHB.PREWORK_PHASES[p].anchor === hash) { phase = AHB.PREWORK_PHASES[p]; break; }
        }
        if (phase) {
          for (var pi = 0; pi < phase.ids.length && !targetItem; pi++) {
            for (var bi = 0; bi < boxes.length; bi++) {
              if (boxes[bi].getAttribute("data-check-id") === phase.ids[pi] && !boxes[bi].checked) {
                targetItem = boxes[bi].closest("[data-check-item]");
                break;
              }
            }
          }
        }
      }
      if (!targetItem && !target) {
        for (var i = 0; i < boxes.length; i++) {
          if (isRequiredId(b, boxes[i].getAttribute("data-check-id")) && !boxes[i].checked) {
            targetItem = boxes[i].closest("[data-check-item]");
            break;
          }
        }
      }
      if (target) {
        var lane = target.closest && target.closest("details");
        if (lane) lane.open = true;
      }
      if (targetItem) {
        var targetLane = targetItem.closest("details");
        if (targetLane) targetLane.open = true;
        setCheckDetail(targetItem.querySelector(".check-detail"), true);
      }
      var scrollTarget = phaseTarget && targetItem ? targetItem : target;
      if (scrollTarget && scrollTarget.scrollIntoView) {
        window.setTimeout(function () { scrollTarget.scrollIntoView({ block: "start" }); }, 0);
      }
    }

    openHashTarget(location.hash);
    window.addEventListener("hashchange", function () { openHashTarget(location.hash); });
  }

  function initForm(form) {
    var key = form.getAttribute("data-storage-key");
    if (!key) return;
    var state = AHB.readState(key);
    var b = null;
    for (var i = 0; i < AHB.REGISTRY.length; i++) {
      if (AHB.REGISTRY[i].key === key) { b = AHB.REGISTRY[i]; break; }
    }
    var boxes = form.querySelectorAll('input[type="checkbox"][data-check-id]');
    Array.prototype.forEach.call(boxes, function (input) {
      var id = input.getAttribute("data-check-id");
      var item = input.closest("[data-check-item]");
      if (b && !isRequiredId(b, id) && item) {
        var stretch = b.stretchIds.indexOf(id) !== -1;
        item.classList.add(stretch ? "is-optional" : "is-conditional");
        var title = item.querySelector(".check-title");
        if (title && !title.querySelector(".check-kind")) {
          var badge = document.createElement("span");
          badge.className = "check-kind";
          badge.textContent = stretch ? "Optional" :
            (/^r-/.test(id) ? "Only if needed" : "Reference");
          title.appendChild(badge);
        }
      }
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
    initPreworkSections(form, b);
    initPreworkStepDetails(form, b);
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
            function (el) {
              var lane = el.closest("details");
              if (lane) lane.open = true;
              setCheckDetail(el, true);
            }
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
            function (el) { setCheckDetail(el, false); }
          );
          Array.prototype.forEach.call(
            document.querySelectorAll("[data-phase-section]"),
            function (section) { setPreworkSection(section, false); }
          );
          Array.prototype.forEach.call(
            document.querySelectorAll("details.lane-disclosure"),
            function (lane) { lane.open = false; }
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
    var weekComplete = AHB.courseComplete();

    if (panel) {
      var done = AHB.countDone(cur);
      var total = cur.ids.length || 1;
      var pct = Math.round((done / total) * 100);
      var isInstall = cur.kind === "install";
      var prework = isInstall ? AHB.preworkProgress() : null;
      setText("[data-yah-eyebrow]", weekComplete
        ? "Friday · Course complete"
        : isInstall
        ? "Monday morning · B0 install clinic"
        : dayLabel(cur) + " · " + cur.code);
      setText("[data-yah-title]", weekComplete
        ? "Week complete"
        : isInstall ? "Install and verify the course setup" : cur.title);
      setText("[data-yah-line]", weekComplete
        ? AHB.TOTAL_MODULES + " / " + AHB.TOTAL_MODULES + " modules complete"
        : isInstall
        ? prework.donePhases + " / " + prework.totalPhases + " phases complete"
        : done + " / " + total + " checks · " + pct + "%");
      var bar = document.querySelector("[data-yah-bar]");
      if (bar) bar.style.width = (weekComplete ? 100 : pct) + "%";
      var cta = document.querySelector("[data-yah-cta]");
      if (cta) {
        cta.textContent = weekComplete
          ? "Review the week map"
          : isInstall
          ? (done > 0 ? "Continue B0" : "Start B0")
          : (done > 0 ? "Continue this module" : "Start this module");
        cta.setAttribute("href", weekComplete
          ? prefix + "/index.html#journey"
          : prefix + "/" + cur.url);
      }
    }

    if (board) {
      var html = "";
      AHB.JOURNEY.forEach(function (col) {
        var hasCurrent = !weekComplete && col.codes.indexOf(cur.code) !== -1;
        html += '<div class="journey-col">';
        html += '<div class="journey-head' + (hasCurrent ? " is-current" : "") + '">';
        html += '<p class="journey-phase">' + col.phase + "</p>";
        html += '<p class="journey-title">' + col.title + "</p>";
        html += "</div>";
        html += '<div class="journey-cells">';
        col.codes.forEach(function (code) {
          var b = AHB.block(code);
          var st = statusOf(b, cur);
          var meta = b.kind === "install" ? b.meta : b.slot;
          html += '<a class="journey-cell is-' + st + '"' +
            (st === "current" ? ' aria-current="step"' : "") +
            ' href="' + prefix + "/" + b.url + '">';
          html += dotHtml(st);
          html += "<span>";
          html += '<span class="journey-name">' +
            b.code + " · " + b.name + "</span>";
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
      var pw = AHB.preworkProgress();
      stat.textContent = pw.donePhases + " / " + pw.totalPhases + " phases complete";
      stat.classList.toggle("is-done", pw.complete);
    }
  }

  /* ---------- pre-work hub ---------- */

  function renderPreworkHub(prefix) {
    var hub = document.querySelector("[data-prework-hub]");
    if (!hub) return;

    var prework = AHB.preworkProgress();
    var pct = Math.round((prework.requiredDone / prework.requiredTotal) * 100);
    var started = prework.requiredDone > 0;

    setText("[data-hub-headline]", prework.complete
      ? "Pre-work setup verified"
      : started ? "Keep moving through the phases" : "Start with the machine");
    setText("[data-hub-line]", prework.donePhases + " / " + prework.totalPhases + " phases complete");
    var bar = document.querySelector("[data-hub-bar]");
    if (bar) bar.style.width = pct + "%";
    var cta = document.querySelector("[data-hub-cta]");
    if (cta) {
      if (prework.complete) {
        cta.textContent = "Next · First Light";
        cta.setAttribute("href", prefix + "/blocks/b1.html");
      } else if (started) {
        cta.textContent = "Continue · " + prework.firstPhase.title;
        cta.setAttribute("href", prefix + "/checklists/prework-install.html#ahb-prework-install-" + prework.firstId);
      } else {
        cta.textContent = "Start phase 1";
        cta.setAttribute("href", prefix + "/checklists/prework-install.html#ahb-prework-install-i-time");
      }
    }

    prework.phases.forEach(function (phase, index) {
      var card = document.querySelector('[data-phase="' + phase.id + '"]');
      if (!card) return;
      var currentPhase = !phase.complete && prework.firstPhase && prework.firstPhase.id === phase.id;
      card.classList.remove("is-done", "is-current");
      if (phase.complete) card.classList.add("is-done");
      else if (currentPhase) card.classList.add("is-current");
      if (currentPhase) card.setAttribute("aria-current", "step");
      else card.removeAttribute("aria-current");
      var stat = card.querySelector("[data-stage-stat]");
      if (stat) {
        stat.textContent = phase.complete
          ? "✓ Complete"
          : (currentPhase ? "Current · " : "") + phase.done + " / " + phase.total;
        stat.classList.remove("stat-done", "stat-current");
        if (phase.complete) stat.classList.add("stat-done");
        else if (currentPhase) stat.classList.add("stat-current");
      }
      card.setAttribute("aria-label", "Phase " + (index + 1) + ": " + phase.title +
        (phase.complete ? ", complete" : currentPhase ? ", current, " : ", ") +
        (phase.complete ? "" : phase.done + " of " + phase.total + " checks"));
    });
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
      // ASCII art inside .diagram is an illustration, not something to paste,
      // so it stays without a button. Everything else in the main column gets
      // one, whether or not the author wrapped the contents in <code>.
      if (pre.closest(".diagram") || pre.querySelector(".copy-btn")) return;
      var code = pre.querySelector("code");
      // Snapshot the text before the button becomes a child of the <pre>,
      // so the button's own label can never end up in the copied text.
      var plain = code ? null : pre.textContent;
      pre.classList.add("has-copy");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy this block to the clipboard");
      btn.addEventListener("click", function () {
        var text = (code ? code.textContent : plain).replace(/\s+$/, "");
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
