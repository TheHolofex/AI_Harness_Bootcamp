/**
 * Friday open-endpoint chat client.
 * Talks to the course host proxy at /__api/chat (HF_TOKEN stays server-side).
 */
(function () {
  "use strict";

  var statusEl = document.getElementById("chat-status");
  var modelEl = document.getElementById("chat-model");
  var baseEl = document.getElementById("chat-base");
  var logEl = document.getElementById("chat-log");
  var formEl = document.getElementById("chat-form");
  var inputEl = document.getElementById("chat-input");
  var sendEl = document.getElementById("chat-send");
  var clearEl = document.getElementById("chat-clear");
  var errorEl = document.getElementById("chat-error");
  var hintEl = document.getElementById("chat-hint");

  if (!formEl || !logEl || !inputEl) return;

  var state = {
    model: "",
    configured: false,
    busy: false,
    messages: [],
    abort: null
  };

  function setError(msg) {
    if (!errorEl) return;
    if (!msg) {
      errorEl.hidden = true;
      errorEl.textContent = "";
      return;
    }
    errorEl.hidden = false;
    errorEl.textContent = msg;
  }

  function setBusy(busy) {
    state.busy = busy;
    var ready = state.configured && !busy;
    inputEl.disabled = !ready;
    sendEl.disabled = !ready;
    clearEl.disabled = busy || state.messages.length === 0;
    sendEl.textContent = busy ? "Sending…" : "Send";
  }

  function renderEmpty() {
    logEl.innerHTML = "";
    var p = document.createElement("p");
    p.className = "friday-chat-empty";
    p.textContent = state.configured
      ? "No messages yet. Ask something short to smoke-check the open endpoint."
      : "Chat is offline until HF_TOKEN is set on the host.";
    logEl.appendChild(p);
  }

  function appendMessage(role, content, streaming) {
    var empty = logEl.querySelector(".friday-chat-empty");
    if (empty) empty.remove();

    var wrap = document.createElement("article");
    wrap.className = "friday-msg friday-msg-" + role;

    var roleEl = document.createElement("div");
    roleEl.className = "friday-msg-role";
    roleEl.textContent = role === "user" ? "You" : role === "assistant" ? "Open model" : "System";

    var body = document.createElement("p");
    body.className = "friday-msg-body";
    if (streaming) body.classList.add("is-streaming");
    body.textContent = content || "";

    wrap.appendChild(roleEl);
    wrap.appendChild(body);
    logEl.appendChild(wrap);
    logEl.scrollTop = logEl.scrollHeight;
    return body;
  }

  function apiRoot() {
    // Page lives at /site/friday-chat.html → host APIs are one level up.
    return window.location.origin;
  }

  async function loadConfig() {
    statusEl.textContent = "Checking…";
    try {
      var res = await fetch(apiRoot() + "/__api/chat/config", {
        credentials: "same-origin",
        headers: { Accept: "application/json" }
      });
      if (res.status === 401) {
        statusEl.textContent = "Sign in required";
        modelEl.textContent = "—";
        baseEl.textContent = "—";
        setError("Session expired or missing. Sign in at /__login, then reload this page.");
        setBusy(false);
        renderEmpty();
        return;
      }
      if (!res.ok) {
        throw new Error("config HTTP " + res.status);
      }
      var cfg = await res.json();
      state.configured = !!cfg.configured;
      state.model = cfg.model || "";
      modelEl.textContent = state.model || "—";
      baseEl.textContent = cfg.base_url || "—";
      if (state.configured) {
        statusEl.textContent = "Ready";
        hintEl.innerHTML = "Streaming via <code>/__api/chat</code> · token stays on the host.";
        setError("");
      } else {
        statusEl.textContent = "HF_TOKEN missing";
        hintEl.textContent = "Add HF_TOKEN to the host .env and restart server.py.";
        setError("Host has no HF_TOKEN. Chat cannot reach Hugging Face until it is set.");
      }
      setBusy(false);
      if (state.messages.length === 0) renderEmpty();
      if (state.configured) inputEl.focus();
    } catch (err) {
      statusEl.textContent = "Unreachable";
      setError("Could not reach chat config: " + (err && err.message ? err.message : err));
      setBusy(false);
      renderEmpty();
    }
  }

  function extractDelta(parsed) {
    if (!parsed || !parsed.choices || !parsed.choices.length) return "";
    var choice = parsed.choices[0] || {};
    if (choice.delta && typeof choice.delta.content === "string") {
      return choice.delta.content;
    }
    if (choice.message && typeof choice.message.content === "string") {
      return choice.message.content;
    }
    // Some providers put text content parts in arrays.
    var content = (choice.delta && choice.delta.content) || (choice.message && choice.message.content);
    if (Array.isArray(content)) {
      return content
        .map(function (part) {
          if (typeof part === "string") return part;
          if (part && typeof part.text === "string") return part.text;
          return "";
        })
        .join("");
    }
    return "";
  }

  async function streamChat(messages, onDelta) {
    var controller = new AbortController();
    state.abort = controller;

    var res = await fetch(apiRoot() + "/__api/chat", {
      method: "POST",
      credentials: "same-origin",
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream, application/json"
      },
      body: JSON.stringify({
        model: state.model || undefined,
        stream: true,
        messages: messages
      })
    });

    if (!res.ok) {
      var errText = await res.text();
      var detail = errText;
      try {
        var ej = JSON.parse(errText);
        if (ej && ej.error) detail = ej.error;
      } catch (_) { /* keep raw */ }
      throw new Error(detail || ("HTTP " + res.status));
    }

    var ctype = (res.headers.get("Content-Type") || "").toLowerCase();
    if (ctype.indexOf("application/json") !== -1) {
      var data = await res.json();
      var full = extractDelta(data) || "";
      if (!full && data && data.choices && data.choices[0] && data.choices[0].message) {
        full = data.choices[0].message.content || "";
      }
      if (full) onDelta(full);
      return full;
    }

    if (!res.body || !res.body.getReader) {
      var fallback = await res.text();
      onDelta(fallback);
      return fallback;
    }

    var reader = res.body.getReader();
    var decoder = new TextDecoder("utf-8");
    var buffer = "";
    var assembled = "";

    while (true) {
      var step = await reader.read();
      if (step.done) break;
      buffer += decoder.decode(step.value, { stream: true });

      var parts = buffer.split("\n");
      buffer = parts.pop() || "";

      for (var i = 0; i < parts.length; i++) {
        var line = parts[i].replace(/\r$/, "");
        if (!line || line.charAt(0) === ":") continue;
        if (line.indexOf("data:") !== 0) continue;
        var payload = line.slice(5).trim();
        if (!payload) continue;
        if (payload === "[DONE]") {
          buffer = "";
          break;
        }
        try {
          var parsed = JSON.parse(payload);
          var delta = extractDelta(parsed);
          if (delta) {
            assembled += delta;
            onDelta(delta);
          }
        } catch (_) {
          // Ignore malformed SSE chunks; keep reading.
        }
      }
    }

    return assembled;
  }

  formEl.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (state.busy || !state.configured) return;

    var text = (inputEl.value || "").trim();
    if (!text) return;

    setError("");
    state.messages.push({ role: "user", content: text });
    appendMessage("user", text, false);
    inputEl.value = "";
    setBusy(true);

    var bodyEl = appendMessage("assistant", "", true);
    var got = "";

    streamChat(state.messages, function (delta) {
      got += delta;
      bodyEl.textContent = got;
      logEl.scrollTop = logEl.scrollHeight;
    })
      .then(function (finalText) {
        var content = (finalText || got || "").trim();
        bodyEl.classList.remove("is-streaming");
        if (!content) {
          content = "(empty response)";
          bodyEl.textContent = content;
        }
        state.messages.push({ role: "assistant", content: content });
      })
      .catch(function (err) {
        bodyEl.classList.remove("is-streaming");
        var msg = err && err.message ? err.message : String(err);
        if (err && err.name === "AbortError") msg = "Request cancelled.";
        bodyEl.textContent = "Error: " + msg;
        bodyEl.parentElement.classList.remove("friday-msg-assistant");
        bodyEl.parentElement.classList.add("friday-msg-system");
        setError(msg);
        // Drop the failed user turn so a retry can re-send cleanly.
        if (state.messages.length && state.messages[state.messages.length - 1].role === "user") {
          state.messages.pop();
        }
      })
      .finally(function () {
        state.abort = null;
        setBusy(false);
        inputEl.focus();
      });
  });

  inputEl.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter" && !ev.shiftKey) {
      ev.preventDefault();
      formEl.requestSubmit();
    }
  });

  clearEl.addEventListener("click", function () {
    if (state.busy) return;
    state.messages = [];
    setError("");
    renderEmpty();
    clearEl.disabled = true;
    inputEl.focus();
  });

  setBusy(true);
  renderEmpty();
  loadConfig();
})();
