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
    if (b.kind === "discussion") return b.title + " · 30-minute discussion";
    if (b.kind === "briefing") return b.code + " · " + b.title;
    return b.slot === "read" || b.slot === "pre" ? b.title : b.code + " · " + b.title;
  }

  function isScheduledBriefing(b) {
    return b.kind === "discussion" || b.kind === "briefing";
  }

  function scheduledStopName(b) {
    return b.kind === "discussion" ? "Discussion" : "Presentation";
  }

  function dayLabel(b) {
    return b.slot === "read" || b.slot === "pre" ? b.day : b.day + " " + b.slot;
  }

  /* ---------- primary nav ---------- */

  function pageOwnerCode(current) {
    if (current === "prework-install") return "B0";
    if (current === "prework" || current === "keys") return "PREWORK";
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
        var navName = isScheduledBriefing(b)
          ? "<strong>" + scheduledStopName(b) + "</strong> · " + b.name
          : "<strong>" + b.code + "</strong> · " + b.name;
        var navSlot = isScheduledBriefing(b) ? "30 min" : b.slot;
        html += '<a class="nav-drop-item' + (st === "done" ? " is-done" : "") + '"' +
          ' href="' + p + "/" + b.url + '"' + (isHere ? ' aria-current="page"' : "") + ">";
        html += dotHtml(st);
        html += '<span class="nav-drop-name">' + navName + "</span>";
        html += '<span class="nav-drop-slot">' + navSlot + "</span>";
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
      var label = b.contextLabel || (b.kind === "install"
        ? "Monday AM · B0 · Pre-work Install Clinic"
        : dayLabel(b) + " · Module " + AHB.moduleNumber(b.code) +
          " of " + AHB.TOTAL_MODULES);
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

    var form = document.querySelector('form[data-storage-key="' + key + '"]');
    var state = AHB.readState(key);
    var outcomeStatuses = form
      ? form.querySelectorAll("[data-outcome-status-for]")
      : [];
    Array.prototype.forEach.call(outcomeStatuses, function (row) {
      var id = row.getAttribute("data-outcome-status-for");
      var complete = state[id] === true;
      row.classList.toggle("is-complete", complete);
      row.classList.toggle("is-remaining", !complete);
      var mark = row.querySelector("[data-outcome-status-mark]");
      var word = row.querySelector("[data-outcome-status-word]");
      if (mark) mark.textContent = complete ? "✓" : "○";
      if (word) word.textContent = complete ? "Complete" : "Not yet";
    });

    var sections = document.querySelectorAll("[data-check-section]");
    Array.prototype.forEach.call(sections, function (section) {
      var name = section.getAttribute("data-check-section");
      var boxes = name === "floor"
        ? (form ? form.querySelectorAll('input[type="checkbox"][data-check-group="floor"][data-check-id]') : [])
        : section.querySelectorAll('input[type="checkbox"][data-check-id]');
      var total = 0, done = 0;
      Array.prototype.forEach.call(boxes, function (box) {
        if (name !== "floor" && box.closest("[data-check-section]") !== section) return;
        if (name !== "floor" && box.getAttribute("data-check-group")) return;
        if (!isRequiredId(b, box.getAttribute("data-check-id"))) return;
        total++;
        if (box.checked) done++;
      });
      var counts = document.querySelectorAll('[data-count-for="' + name + '"]');
      Array.prototype.forEach.call(counts, function (el) {
        el.textContent = done + "/" + total;
      });
    });

    if (form) {
      updateExerciseStageStatuses(form, b);
      updateExerciseNavigator(form, b);
    }

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

  function prepareOutcomeLayout(form, b) {
    if (!form || !b) return;
    var section = form.querySelector('#floor[data-check-section="floor"]');
    if (!section) return;
    var sources = Array.prototype.slice.call(section.querySelectorAll("ol.checklist"));
    if (!sources.length) return;
    var entries = [];
    sources.forEach(function (source) {
      var sourceItems = Array.prototype.slice.call(source.querySelectorAll("[data-check-item]"));
      sourceItems.forEach(function (item) {
        entries.push({ item: item, source: source });
      });
    });
    if (!entries.length) return;

    var valid = true;
    entries.forEach(function (entry) {
      var item = entry.item;
      var target = item.getAttribute("data-outcome-after");
      var input = item.querySelector('input[type="checkbox"][data-check-id]');
      var title = item.querySelector(".check-title");
      var anchor = null;
      var replacedItem = null;
      if (target && target.charAt(0) === "#") {
        anchor = form.querySelector(target);
      } else if (target) {
        var targetInput = form.querySelector('input[data-check-id="' + target + '"]');
        var targetItem = targetInput && targetInput.closest("[data-check-item]");
        anchor = targetItem && targetItem.closest("ol.checklist");
        replacedItem = targetItem;
      }
      if (!input || !title || !target || !anchor || section.contains(anchor)) {
        valid = false;
        return;
      }
      entry.input = input;
      entry.title = title;
      entry.detail = item.querySelector(".check-detail");
      entry.target = target;
      entry.anchor = anchor;
      entry.replacedItem = replacedItem;
    });
    if (!valid) return;

    sources.forEach(function (source) {
      source.classList.remove("checklist");
      source.classList.add("outcome-summary");
      source.setAttribute("aria-label", "Lesson outcome status");
    });
    var groups = [];

    entries.forEach(function (entry) {
      var item = entry.item;
      var source = entry.source;
      var input = entry.input;
      var title = entry.title;
      var detail = entry.detail;
      var target = entry.target;
      var anchor = entry.anchor;

      var group = null;
      for (var gi = 0; gi < groups.length; gi++) {
        if (groups[gi].anchor === anchor) {
          group = groups[gi].group;
          break;
        }
      }
      if (!group) {
        group = document.createElement("div");
        group.className = "inline-outcomes";
        group.setAttribute("data-inline-outcomes-for", target);
        var list = document.createElement("ol");
        list.className = "checklist outcome-checklist";
        list.setAttribute("aria-label", "Lesson outcome to confirm here");
        group.appendChild(list);
        anchor.insertAdjacentElement("afterend", group);
        groups.push({ anchor: anchor, group: group });
      }

      var id = input.getAttribute("data-check-id");
      var optional = b.stretchIds.indexOf(id) !== -1;
      var summary = document.createElement("li");
      summary.className = "outcome-status" + (optional ? " is-optional" : "");
      summary.setAttribute("data-outcome-status-for", id);
      var summaryMark = document.createElement("span");
      summaryMark.className = "outcome-status-mark";
      summaryMark.setAttribute("data-outcome-status-mark", "");
      summaryMark.setAttribute("aria-hidden", "true");
      summaryMark.textContent = "○";
      var summaryBody = document.createElement("div");
      summaryBody.className = "outcome-status-body";
      var summaryTitle = document.createElement("a");
      summaryTitle.className = "outcome-status-title";
      summaryTitle.setAttribute("href", "#" + input.id);
      summaryTitle.innerHTML = title.innerHTML;
      Array.prototype.forEach.call(summaryTitle.querySelectorAll(".tag, .check-kind"), function (tag) {
        tag.insertAdjacentText("afterend", " ");
      });
      summaryTitle.addEventListener("click", function () {
        var lane = input.closest("details");
        if (lane) lane.open = true;
        var exerciseStage = input.closest("[data-exercise-stage]");
        if (exerciseStage) setExerciseStage(exerciseStage, true);
      });
      if (optional) {
        var optionalBadge = document.createElement("span");
        optionalBadge.className = "check-kind";
        optionalBadge.textContent = "Optional";
        summaryTitle.appendChild(document.createTextNode(" "));
        summaryTitle.appendChild(optionalBadge);
      }
      summaryBody.appendChild(summaryTitle);
      if (detail) {
        var summaryDetail = document.createElement("div");
        summaryDetail.className = "outcome-status-detail";
        summaryDetail.innerHTML = detail.innerHTML;
        summaryBody.appendChild(summaryDetail);
      }
      var summaryWord = document.createElement("span");
      summaryWord.className = "outcome-status-word";
      summaryWord.setAttribute("data-outcome-status-word", "");
      summaryWord.textContent = "Not yet";
      summary.appendChild(summaryMark);
      summary.appendChild(summaryBody);
      summary.appendChild(summaryWord);
      source.appendChild(summary);

      input.setAttribute("data-check-group", "floor");
      if (entry.replacedItem) {
        input.setAttribute("data-replaces-check-id", entry.target);
      }
      item.classList.add("outcome-check");
      item.setAttribute("data-outcome-item", "");
      var number = item.querySelector(".check-num");
      if (number) {
        number.classList.remove("check-num");
        number.classList.add("outcome-check-label");
        number.textContent = optional ? "Optional outcome" : "Lesson outcome";
      }
      group.querySelector("ol").appendChild(item);
    });

    // A lesson outcome is the receipt for the evidence-producing step. When an
    // outcome targets a procedural checkbox, showing both controls asks the
    // learner to confirm the same evidence twice. Keep the instructions in
    // place, move the outcome control beside them, and hide only the duplicate
    // procedural receipt. Hash targets are ordinary anchors and stay visible.
    var replacedItems = [];
    entries.forEach(function (entry) {
      var replacedItem = entry.replacedItem;
      if (!replacedItem || replacedItems.indexOf(replacedItem) !== -1) return;
      replacedItems.push(replacedItem);
      replacedItem.hidden = true;
      replacedItem.setAttribute("data-replaced-by-outcome", "");
    });

    if (location.hash) {
      var hash = "";
      try { hash = decodeURIComponent(location.hash.replace(/^#/, "")); }
      catch (e) { hash = location.hash.replace(/^#/, ""); }
      var hashTarget = hash ? document.getElementById(hash) : null;
      if (hashTarget && hashTarget.closest("[data-outcome-item]")) {
        var hashLane = hashTarget.closest("details");
        if (hashLane) hashLane.open = true;
        window.setTimeout(function () {
          hashTarget.scrollIntoView({ block: "center" });
          hashTarget.focus();
        }, 0);
      }
    }
  }

  function setPreworkSection(section, open) {
    if (!section) return;
    section.classList.toggle("is-section-collapsed", !open);
    var button = section.querySelector("[data-phase-section-toggle]");
    if (button) button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function isStagedExercise(b) {
    return !!(b && /^(?:B1|PI|P[1-8])$/.test(b.code));
  }

  function setExerciseStage(stage, open) {
    if (!stage) return;
    var body = stage.querySelector("[data-exercise-stage-body]");
    var button = stage.querySelector("[data-exercise-stage-toggle]");
    stage.classList.toggle("is-section-collapsed", !open);
    if (body) body.hidden = !open;
    if (button) button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function updateExerciseStageStatuses(form, b) {
    if (!form || !isStagedExercise(b)) return;
    var mission = form.querySelector('#mission[data-check-section="mission"]');
    if (!mission) return;
    var stages = Array.prototype.slice.call(
      form.querySelectorAll("[data-exercise-stage]")
    );
    if (!stages.length) return;

    var progress = stages.map(function (stage) {
      var boxes = stage.querySelectorAll('input[type="checkbox"][data-check-id]');
      var done = 0, total = 0, pendingReflection = 0;
      Array.prototype.forEach.call(boxes, function (box) {
        if (!isRequiredId(b, box.getAttribute("data-check-id"))) return;
        if (box.closest('[data-check-section="pulse"]')) {
          if (!box.checked) pendingReflection++;
          return;
        }
        total++;
        if (box.checked) done++;
      });
      return {
        type: "stage",
        root: stage,
        stage: stage,
        done: done,
        total: total,
        pendingReflection: pendingReflection,
        complete: total > 0 && done === total && pendingReflection === 0,
        laterStageStarted: false
      };
    });

    var sequence = [];
    Array.prototype.forEach.call(
      mission.querySelectorAll("[data-exercise-stage], .lesson-reflection"),
      function (root) {
        if (root.matches("[data-exercise-stage]")) {
          for (var si = 0; si < progress.length; si++) {
            if (progress[si].stage === root) {
              sequence.push(progress[si]);
              break;
            }
          }
          return;
        }
        if (root.closest("[data-exercise-stage]")) return;
        var boxes = root.querySelectorAll('input[type="checkbox"][data-check-id]');
        var done = 0, total = 0;
        Array.prototype.forEach.call(boxes, function (box) {
          if (!isRequiredId(b, box.getAttribute("data-check-id"))) return;
          total++;
          if (box.checked) done++;
        });
        sequence.push({
          type: "reflection",
          root: root,
          done: done,
          total: total,
          pendingReflection: 0,
          complete: total > 0 && done === total,
          laterStageStarted: false
        });
      }
    );

    // A route item with no receipt stays visually neutral. Later progress can
    // move the current marker forward, but it cannot manufacture evidence.
    for (var i = 0; i < sequence.length; i++) {
      if (sequence[i].total > 0) continue;
      for (var j = i + 1; j < sequence.length; j++) {
        if (sequence[j].done > 0) {
          sequence[i].laterStageStarted = true;
          break;
        }
      }
    }

    var current = null;
    sequence.forEach(function (item) {
      if (!item.complete && !item.laterStageStarted && !current) current = item;
      item.root.classList.toggle("is-section-done", item.complete);
      item.root.classList.toggle("is-section-past", item.laterStageStarted);
      item.root.classList.remove("is-section-current");
      item.root.setAttribute("data-exercise-done", item.done);
      item.root.setAttribute("data-exercise-total", item.total);
      item.root.setAttribute("data-exercise-status", item.complete
        ? "complete"
        : (item.laterStageStarted
          ? "instructions"
          : (item.type === "reflection" && !item.total ? "review" : "not-complete")));
    });

    progress.forEach(function (item) {
      var stat = item.stage.querySelector("[data-exercise-stage-stat]");
      var isCurrent = current === item;
      if (isCurrent) {
        item.stage.classList.add("is-section-current");
        item.stage.setAttribute("data-exercise-status", "next");
      }
      if (stat) {
        if (item.complete) stat.textContent = "✓ Complete";
        else if (isCurrent && item.done === item.total && item.pendingReflection) {
          stat.textContent = "Next unfinished · Reflection remains";
        } else if (!item.total) {
          stat.textContent = isCurrent
            ? "Next unfinished · Run this stage"
            : (item.laterStageStarted ? "Instructions" : "Run this stage");
        } else if (isCurrent) {
          stat.textContent = "Next unfinished · " + item.done + " / " + item.total;
        } else {
          stat.textContent = item.done + " / " + item.total;
        }
      }
    });

    sequence.forEach(function (item) {
      if (item.type !== "reflection" || current !== item) return;
      item.root.classList.add("is-section-current");
      item.root.setAttribute("data-exercise-status", item.total ? "next" : "review");
    });

    if (current && current.type === "stage") setExerciseStage(current.stage, true);
  }

  function initExerciseStages(form, b) {
    if (!form || !isStagedExercise(b)) return;
    var mission = form.querySelector('#mission[data-check-section="mission"]');
    if (!mission) return;

    var headings = [];
    Array.prototype.forEach.call(mission.children, function (child) {
      if (child.tagName === "H3" && /^Stage\s+\d+\s*·/i.test(child.textContent.trim())) {
        headings.push(child);
      }
    });
    if (!headings.length) return;

    headings.forEach(function (heading, index) {
      var nextHeading = headings[index + 1] || null;
      var boundary = nextHeading;
      var stageNumber = (heading.textContent.trim().match(/^Stage\s+(\d+)/i) || [])[1];
      var reflection = null;
      var continuation = false;
      var scan = heading.nextElementSibling;
      while (scan && scan !== nextHeading) {
        if (scan.matches && scan.matches(".lesson-reflection")) {
          reflection = scan;
        } else if (reflection && scan.tagName === "H3" && stageNumber &&
          new RegExp("^Finish\\s+Stage\\s+0*" + parseInt(stageNumber, 10) + "\\b", "i")
            .test(scan.textContent.trim())) {
          continuation = true;
        }
        scan = scan.nextElementSibling;
      }
      if (reflection && !continuation) boundary = reflection;

      var stage = document.createElement("section");
      stage.className = "exercise-stage is-section-collapsed";
      stage.setAttribute("data-exercise-stage", "");
      mission.insertBefore(stage, heading);
      stage.appendChild(heading);

      var stageSlug = b.code.toLowerCase() + "-stage-" + (index + 1);
      if (!heading.id) heading.id = stageSlug;
      heading.classList.add("phase-section-heading", "exercise-stage-heading");

      var title = document.createElement("span");
      title.className = "phase-section-title";
      while (heading.firstChild) title.appendChild(heading.firstChild);

      var button = document.createElement("button");
      button.type = "button";
      button.className = "phase-section-toggle";
      button.id = stageSlug + "-toggle";
      button.setAttribute("data-exercise-stage-toggle", "");
      button.setAttribute("aria-expanded", "false");

      var stat = document.createElement("span");
      stat.className = "phase-section-stat";
      stat.setAttribute("data-exercise-stage-stat", "");
      stat.textContent = "0 / 0";
      var cue = document.createElement("span");
      cue.className = "phase-section-cue";
      cue.setAttribute("aria-hidden", "true");
      button.appendChild(title);
      button.appendChild(stat);
      button.appendChild(cue);
      heading.appendChild(button);

      var body = document.createElement("div");
      body.className = "exercise-stage-body";
      body.id = stageSlug + "-body";
      body.setAttribute("data-exercise-stage-body", "");
      button.setAttribute("aria-controls", body.id);
      stage.appendChild(body);

      while (stage.nextSibling && stage.nextSibling !== boundary) {
        body.appendChild(stage.nextSibling);
      }
      setExerciseStage(stage, false);
      button.addEventListener("click", function () {
        setExerciseStage(stage, button.getAttribute("aria-expanded") !== "true");
      });
    });

    var tools = document.createElement("div");
    tools.className = "exercise-stage-tools";
    tools.setAttribute("role", "group");
    tools.setAttribute("aria-label", "Stage controls");
    var openAll = document.createElement("button");
    openAll.type = "button";
    openAll.className = "btn btn-secondary";
    openAll.textContent = "Open all stages";
    var closeAll = document.createElement("button");
    closeAll.type = "button";
    closeAll.className = "btn btn-secondary";
    closeAll.textContent = "Close all stages";
    tools.appendChild(openAll);
    tools.appendChild(closeAll);
    mission.insertBefore(tools, mission.querySelector("[data-exercise-stage]"));

    var stages = mission.querySelectorAll("[data-exercise-stage]");
    openAll.addEventListener("click", function () {
      Array.prototype.forEach.call(stages, function (stage) { setExerciseStage(stage, true); });
    });
    closeAll.addEventListener("click", function () {
      Array.prototype.forEach.call(stages, function (stage) { setExerciseStage(stage, false); });
    });

    function openHashTarget(rawHash) {
      var hash = "";
      try { hash = decodeURIComponent((rawHash || "").replace(/^#/, "")); }
      catch (e) { hash = (rawHash || "").replace(/^#/, ""); }
      var target = hash ? document.getElementById(hash) : null;
      var stage = target && target.closest ? target.closest("[data-exercise-stage]") : null;
      if (!stage) return;
      setExerciseStage(stage, true);
      window.setTimeout(function () { target.scrollIntoView({ block: "start" }); }, 0);
    }

    openHashTarget(location.hash);
    window.addEventListener("hashchange", function () { openHashTarget(location.hash); });
  }

  function exerciseNavigatorTitle(text) {
    return (text || "")
      .replace(/^Stage\s+\d+\s*·\s*/i, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function exerciseReflectionTitle(root) {
    var question = root && root.querySelector(".reflection-question");
    if (!question) return "Review the lesson pattern before moving on";
    return (question.textContent || "")
      .replace(/^(?:Closeout question|Think back|Workplace rule):\s*/i, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function replaceExerciseHash(id) {
    if (!id || !window.history || !window.history.replaceState) return;
    try {
      window.history.replaceState(window.history.state, "", "#" + encodeURIComponent(id));
    } catch (e) { /* file previews can deny History API writes */ }
  }

  function exerciseRouteStatus(record) {
    return record.root.getAttribute("data-exercise-status") || "not-complete";
  }

  function exerciseRouteLabel(record) {
    return record.type === "stage"
      ? "Stage " + record.stageNumber
      : "Lesson reflection";
  }

  function setExerciseNavigatorVisible(state, visible) {
    var wasHidden = state.nav.hidden;
    state.nav.hidden = !visible;
    document.body.classList.toggle("has-exercise-navigator", visible);
    if (visible && wasHidden) {
      window.setTimeout(function () {
        updateExerciseNavigator(state.form, state.block);
      }, 0);
    }
  }

  function setExerciseNavigatorText(element, value) {
    if (element.textContent !== value) element.textContent = value;
  }

  function updateExerciseNavigator(form, b) {
    var state = form && form._exerciseNavigator;
    if (!state || !isStagedExercise(b)) return;

    var finishedStages = 0;
    state.records.forEach(function (record) {
      var status = exerciseRouteStatus(record);
      var done = parseInt(record.root.getAttribute("data-exercise-done") || "0", 10);
      var total = parseInt(record.root.getAttribute("data-exercise-total") || "0", 10);
      var active = state.records[state.activeIndex] === record;
      var complete = status === "complete";
      if (record.type === "stage" && (complete || status === "instructions")) {
        finishedStages++;
      }

      record.node.classList.toggle("is-active", active);
      record.node.classList.toggle("is-done", complete);
      record.node.classList.toggle("is-next", status === "next");
      record.node.classList.toggle("is-instructions", status === "instructions");
      record.root.classList.toggle("is-stage-active", active);
      record.mark.textContent = complete ? "✓" :
        (record.type === "stage" ? record.stageNumber : "R");

      var statusLabel = complete
        ? "complete"
        : (status === "next"
          ? "next unfinished step"
          : (status === "instructions"
            ? "instructions passed; no checkbox required"
            : (status === "review"
              ? "read before moving on"
              : (total ? done + " of " + total + " receipts complete" : "not complete"))));
      var activeLabel = active ? ", currently viewed" : "";
      var name = record.type === "stage"
        ? "Stage " + record.stageNumber + " of " + state.stageCount + ", " + record.title
        : "Lesson reflection, " + record.title;
      record.button.setAttribute("aria-label", name + ", " + statusLabel + activeLabel);
      record.button.setAttribute("title", exerciseRouteLabel(record) + " · " + record.title);
      if (active) record.button.setAttribute("aria-current", "step");
      else record.button.removeAttribute("aria-current");
    });

    var activeRecord = state.records[state.activeIndex] || state.records[0];
    if (!activeRecord) return;
    setExerciseNavigatorText(state.kicker, activeRecord.type === "stage"
      ? "Stage " + activeRecord.stageNumber + " of " + state.stageCount
      : "Lesson reflection");
    setExerciseNavigatorText(state.title, activeRecord.title);
    var summary = finishedStages + " of " + state.stageCount + " stages finished";
    if (activeRecord.type === "reflection") {
      var reflectionDone = parseInt(activeRecord.root.getAttribute("data-exercise-done") || "0", 10);
      var reflectionTotal = parseInt(activeRecord.root.getAttribute("data-exercise-total") || "0", 10);
      if (reflectionTotal) summary += " · Reflection " + reflectionDone + "/" + reflectionTotal;
    }
    setExerciseNavigatorText(state.summary, summary);

    var previous = state.activeIndex > 0 ? state.records[state.activeIndex - 1] : null;
    var next = state.activeIndex < state.records.length - 1
      ? state.records[state.activeIndex + 1]
      : null;
    state.previous.disabled = !previous;
    setExerciseNavigatorText(state.previousTarget,
      previous ? exerciseRouteLabel(previous) : "Start");
    state.previous.setAttribute("aria-label", previous
      ? "Previous: " + exerciseRouteLabel(previous) + " — " + previous.title
      : "Previous step unavailable");
    state.next.disabled = !next && !state.outcomes;
    setExerciseNavigatorText(state.nextTarget,
      next ? exerciseRouteLabel(next) : "Lesson outcomes");
    state.next.setAttribute("aria-label", next
      ? "Next: " + exerciseRouteLabel(next) + " — " + next.title
      : "Next: Lesson outcomes");

    var activeButton = activeRecord.button;
    var viewport = state.trackViewport;
    if (activeButton && viewport.clientWidth && viewport.scrollWidth > viewport.clientWidth) {
      var buttonRect = activeButton.getBoundingClientRect();
      var viewportRect = viewport.getBoundingClientRect();
      var targetScrollLeft = viewport.scrollLeft +
        (buttonRect.left - viewportRect.left) -
        (viewport.clientWidth - buttonRect.width) / 2;
      viewport.scrollLeft = Math.max(0, targetScrollLeft);
    }
  }

  function activateExerciseRoute(state, index, updateHash) {
    if (!state || index < 0 || index >= state.records.length) return;
    state.activeIndex = index;
    state.lockUntil = Date.now() + 650;
    if (updateHash) replaceExerciseHash(state.records[index].target.id);
    updateExerciseNavigator(state.form, state.block);
  }

  function navigateToExerciseRoute(state, index) {
    var record = state && state.records[index];
    if (!record) return;
    if (record.stage) setExerciseStage(record.stage, true);
    activateExerciseRoute(state, index, true);
    setExerciseNavigatorVisible(state, true);
    record.target.scrollIntoView({ block: "start" });
  }

  function navigateToExerciseOutcomes(state) {
    if (!state || !state.outcomes) return;
    var heading = state.outcomes.querySelector("h2") || state.outcomes;
    if (!heading.hasAttribute("tabindex")) heading.setAttribute("tabindex", "-1");
    replaceExerciseHash(state.outcomes.id);
    state.lockUntil = Date.now() + 650;
    state.hideUntil = Date.now() + 1200;
    heading.focus();
    heading.scrollIntoView({ block: "start" });
    setExerciseNavigatorVisible(state, false);
    window.setTimeout(function () { syncExerciseNavigatorFromViewport(state); }, 1250);
  }

  function syncExerciseNavigatorFromViewport(state) {
    if (!state || !state.records.length) return;
    if (Date.now() < state.hideUntil) {
      setExerciseNavigatorVisible(state, false);
      return;
    }
    var start = state.mission.querySelector("h2") || state.records[0].target;
    var end = state.records[state.records.length - 1].root;
    // Desktop combines the document scroll padding with each stage's scroll
    // margin, so the stable reading line sits below both sticky nav rows.
    var anchor = window.innerWidth <= 760
      ? 88
      : Math.max(180, Math.min(230, window.innerHeight * 0.34));
    var visible = start.getBoundingClientRect().top <= window.innerHeight * 0.62 &&
      end.getBoundingClientRect().bottom >= anchor;
    setExerciseNavigatorVisible(state, visible);
    if (!visible || Date.now() < state.lockUntil) return;

    var activeIndex = 0;
    for (var i = 0; i < state.records.length; i++) {
      if (state.records[i].target.getBoundingClientRect().top <= anchor) activeIndex = i;
      else break;
    }
    if (activeIndex !== state.activeIndex) {
      state.activeIndex = activeIndex;
      updateExerciseNavigator(state.form, state.block);
    }
  }

  function initExerciseNavigator(form, b) {
    if (!form || !isStagedExercise(b)) return;
    var mission = form.querySelector('#mission[data-check-section="mission"]');
    if (!mission) return;
    var stageCount = mission.querySelectorAll("[data-exercise-stage]").length;
    if (!stageCount) return;

    var records = [];
    var stageNumber = 0;
    Array.prototype.forEach.call(
      mission.querySelectorAll("[data-exercise-stage], .lesson-reflection"),
      function (root) {
        var stage = root.matches("[data-exercise-stage]") ? root : null;
        if (!stage && root.closest("[data-exercise-stage]")) return;
        if (stage) {
          stageNumber++;
          var heading = stage.querySelector(".exercise-stage-heading");
          var title = heading && heading.querySelector(".phase-section-title");
          if (!heading || !title) return;
          records.push({
            type: "stage",
            root: root,
            stage: stage,
            target: heading,
            title: exerciseNavigatorTitle(title.textContent),
            stageNumber: stageNumber
          });
          return;
        }
        if (!root.id) root.id = b.code.toLowerCase() + "-lesson-reflection";
        records.push({
          type: "reflection",
          root: root,
          stage: null,
          target: root,
          title: exerciseReflectionTitle(root),
          stageNumber: null
        });
      }
    );
    if (!records.length) return;

    var nav = document.createElement("nav");
    nav.className = "exercise-progress";
    nav.setAttribute("data-exercise-navigator", "");
    nav.setAttribute("aria-label", "Run of exercise progress");
    nav.hidden = true;

    var head = document.createElement("div");
    head.className = "exercise-progress-head";
    var current = document.createElement("div");
    current.className = "exercise-progress-current";
    var kicker = document.createElement("span");
    kicker.className = "exercise-progress-kicker";
    var currentTitle = document.createElement("strong");
    currentTitle.className = "exercise-progress-title";
    currentTitle.setAttribute("aria-live", "polite");
    currentTitle.setAttribute("aria-atomic", "true");
    var progressSummary = document.createElement("span");
    progressSummary.className = "exercise-progress-summary";
    current.appendChild(kicker);
    current.appendChild(currentTitle);
    current.appendChild(progressSummary);
    head.appendChild(current);
    nav.appendChild(head);

    var controls = document.createElement("div");
    controls.className = "exercise-progress-controls";

    function directionButton(direction, label) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "exercise-progress-direction exercise-progress-" + direction;
      var main = document.createElement("span");
      main.className = "exercise-progress-direction-main";
      main.textContent = direction === "previous" ? "← " + label : label + " →";
      var target = document.createElement("span");
      target.className = "exercise-progress-direction-target";
      button.appendChild(main);
      button.appendChild(target);
      return { button: button, target: target };
    }

    var previousParts = directionButton("previous", "Previous");
    var nextParts = directionButton("next", "Next");
    controls.appendChild(previousParts.button);

    var trackViewport = document.createElement("div");
    trackViewport.className = "exercise-progress-track-viewport";
    var track = document.createElement("ol");
    track.className = "exercise-progress-track";
    track.setAttribute("aria-label", "Exercise timeline");
    records.forEach(function (record, index) {
      var node = document.createElement("li");
      node.className = "exercise-progress-node";
      var button = document.createElement("button");
      button.type = "button";
      button.className = "exercise-progress-node-button";
      if (record.stage) {
        var body = record.stage.querySelector("[data-exercise-stage-body]");
        if (body && body.id) button.setAttribute("aria-controls", body.id);
      } else {
        button.setAttribute("aria-controls", record.root.id);
      }
      var mark = document.createElement("span");
      mark.className = "exercise-progress-node-mark";
      mark.setAttribute("aria-hidden", "true");
      button.appendChild(mark);
      button.addEventListener("click", function () { navigateToExerciseRoute(state, index); });
      node.appendChild(button);
      track.appendChild(node);
      record.node = node;
      record.button = button;
      record.mark = mark;
    });
    trackViewport.appendChild(track);
    controls.appendChild(trackViewport);
    controls.appendChild(nextParts.button);
    nav.appendChild(controls);
    mission.insertBefore(nav, mission.querySelector("[data-exercise-stage]"));

    var outcomes = form.querySelector('#floor[data-check-section="floor"]');
    var state = {
      form: form,
      block: b,
      mission: mission,
      outcomes: outcomes,
      records: records,
      stageCount: stageCount,
      nav: nav,
      kicker: kicker,
      title: currentTitle,
      summary: progressSummary,
      previous: previousParts.button,
      previousTarget: previousParts.target,
      next: nextParts.button,
      nextTarget: nextParts.target,
      trackViewport: trackViewport,
      activeIndex: -1,
      lockUntil: 0,
      hideUntil: 0,
      scrollTimer: null
    };
    form._exerciseNavigator = state;

    var hashTarget = null;
    if (location.hash) {
      var hash = "";
      try { hash = decodeURIComponent(location.hash.replace(/^#/, "")); }
      catch (e) { hash = location.hash.replace(/^#/, ""); }
      hashTarget = hash ? document.getElementById(hash) : null;
    }
    records.forEach(function (record, index) {
      if (state.activeIndex === -1 && hashTarget && record.root.contains(hashTarget)) {
        state.activeIndex = index;
      }
      if (record.stage) {
        var toggle = record.stage.querySelector("[data-exercise-stage-toggle]");
        if (toggle) toggle.addEventListener("click", function () {
          activateExerciseRoute(state, index, true);
        });
      }
    });
    if (state.activeIndex === -1) {
      for (var i = 0; i < records.length; i++) {
        if (records[i].root.classList.contains("is-section-current")) {
          state.activeIndex = i;
          break;
        }
      }
    }
    if (state.activeIndex === -1) state.activeIndex = 0;

    previousParts.button.addEventListener("click", function () {
      navigateToExerciseRoute(state, state.activeIndex - 1);
    });
    nextParts.button.addEventListener("click", function () {
      if (state.activeIndex < state.records.length - 1) {
        navigateToExerciseRoute(state, state.activeIndex + 1);
      } else {
        navigateToExerciseOutcomes(state);
      }
    });

    function scheduleViewportSync() {
      if (state.scrollTimer) return;
      state.scrollTimer = window.setTimeout(function () {
        state.scrollTimer = null;
        syncExerciseNavigatorFromViewport(state);
      }, 60);
    }
    window.addEventListener("scroll", scheduleViewportSync);
    window.addEventListener("resize", scheduleViewportSync);
    window.addEventListener("hashchange", function () {
      var raw = "";
      try { raw = decodeURIComponent(location.hash.replace(/^#/, "")); }
      catch (e) { raw = location.hash.replace(/^#/, ""); }
      var target = raw ? document.getElementById(raw) : null;
      records.forEach(function (record, index) {
        if (target && record.root.contains(target)) activateExerciseRoute(state, index, false);
      });
      scheduleViewportSync();
    });

    updateExerciseNavigator(form, b);
    window.setTimeout(function () { syncExerciseNavigatorFromViewport(state); }, 0);
  }

  function migrateReplacedOutcomeState(form, key, state) {
    var outcomes = form.querySelectorAll(
      'input[data-check-id][data-replaces-check-id]'
    );
    var replacements = {};
    Array.prototype.forEach.call(outcomes, function (input) {
      var oldId = input.getAttribute("data-replaces-check-id");
      var newId = input.getAttribute("data-check-id");
      if (!oldId || !newId || oldId === newId) return;
      if (!replacements[oldId]) replacements[oldId] = [];
      replacements[oldId].push(newId);
    });

    var changed = false;
    Object.keys(replacements).forEach(function (oldId) {
      if (!Object.prototype.hasOwnProperty.call(state, oldId)) return;
      if (state[oldId] === true) {
        replacements[oldId].forEach(function (newId) {
          if (state[newId] !== true) {
            state[newId] = true;
            changed = true;
          }
        });
      }
      delete state[oldId];
      changed = true;
    });

    if (changed) {
      state._updated = new Date().toISOString();
      saveState(key, state);
    }
    return state;
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
    var b = null;
    for (var i = 0; i < AHB.REGISTRY.length; i++) {
      if (AHB.REGISTRY[i].key === key) { b = AHB.REGISTRY[i]; break; }
    }
    prepareOutcomeLayout(form, b);
    var state = migrateReplacedOutcomeState(form, key, AHB.readState(key));
    var boxes = form.querySelectorAll('input[type="checkbox"][data-check-id]');
    Array.prototype.forEach.call(boxes, function (input) {
      var id = input.getAttribute("data-check-id");
      var item = input.closest("[data-check-item]");
      if (b && !isRequiredId(b, id) && item) {
        var stretch = b.stretchIds.indexOf(id) !== -1;
        item.classList.add(stretch ? "is-optional" : "is-conditional");
        var title = item.querySelector(".check-title");
        if (title && !item.hasAttribute("data-outcome-item") && !title.querySelector(".check-kind")) {
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
    initExerciseStages(form, b);
    initPreworkStepDetails(form, b);
    updateProgressOutputs(key);
    initExerciseNavigator(form, b);
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
      var isBriefing = isScheduledBriefing(cur);
      var prework = isInstall ? AHB.preworkProgress() : null;
      setText("[data-yah-eyebrow]", weekComplete
        ? "Friday · Course complete"
        : isInstall
        ? "Monday morning · B0 install clinic"
        : isBriefing
        ? dayLabel(cur) + " · 30-minute " + scheduledStopName(cur).toLowerCase()
        : dayLabel(cur) + " · " + cur.code);
      setText("[data-yah-title]", weekComplete
        ? "Week complete"
        : isInstall ? "Install and verify the course setup" : cur.title);
      setText("[data-yah-line]", weekComplete
        ? AHB.TOTAL_MODULES + " / " + AHB.TOTAL_MODULES + " modules complete"
        : isInstall
        ? prework.donePhases + " / " + prework.totalPhases + " phases complete"
        : isBriefing
        ? cur.meta
        : done + " / " + total + " checks · " + pct + "%");
      var bar = document.querySelector("[data-yah-bar]");
      if (bar) bar.style.width = (weekComplete ? 100 : pct) + "%";
      var cta = document.querySelector("[data-yah-cta]");
      if (cta) {
        cta.textContent = weekComplete
          ? "Review the week map"
          : isInstall
          ? (done > 0 ? "Continue B0" : "Start B0")
          : isBriefing
          ? "Open the " + scheduledStopName(cur).toLowerCase()
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
          var meta = b.kind === "install" || isScheduledBriefing(b) ? b.meta : b.slot;
          var journeyName = isScheduledBriefing(b)
            ? scheduledStopName(b) + " · " + b.name
            : b.code + " · " + b.name;
          html += '<a class="journey-cell is-' + st + '"' +
            (st === "current" ? ' aria-current="step"' : "") +
            ' href="' + prefix + "/" + b.url + '">';
          html += dotHtml(st);
          html += "<span>";
          html += '<span class="journey-name">' + journeyName + "</span>";
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
