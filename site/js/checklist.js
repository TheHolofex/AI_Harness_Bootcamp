
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function loadState(key) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return {};
      const data = JSON.parse(raw);
      return data && typeof data === 'object' ? data : {};
    } catch (e) {
      return {};
    }
  }

  function saveState(key, state) {
    try {
      localStorage.setItem(key, JSON.stringify(state));
    } catch (e) {
      console.warn('checklist save failed', e);
    }
  }

  function updateProgress(form) {
    const key = form.getAttribute('data-storage-key');
    const boxes = qsa('input[type="checkbox"][data-check-id]', form);
    const total = boxes.length || 1;
    const done = boxes.filter((b) => b.checked).length;
    const pct = Math.round((done / total) * 100);
    qsa('[data-progress-for="' + key + '"]').forEach((el) => {
      el.textContent = pct + '% (' + done + '/' + total + ')';
    });
    qsa('[data-progress-bar-for="' + key + '"]').forEach((el) => {
      el.style.width = pct + '%';
    });
  }

  function applyItemState(input) {
    const li = input.closest('[data-check-item]');
    if (!li) return;
    li.classList.toggle('is-done', input.checked);
  }

  function initForm(form) {
    const key = form.getAttribute('data-storage-key');
    if (!key) return;
    const state = loadState(key);
    qsa('input[type="checkbox"][data-check-id]', form).forEach((input) => {
      const id = input.getAttribute('data-check-id');
      input.checked = !!state[id];
      applyItemState(input);
      input.addEventListener('change', () => {
        const s = loadState(key);
        s[id] = input.checked;
        s._updated = new Date().toISOString();
        saveState(key, s);
        applyItemState(input);
        updateProgress(form);
      });
    });
    updateProgress(form);
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Index cards summary
    qsa('[data-checklist-card]').forEach((card) => {
      const key = card.getAttribute('data-storage-key');
      const total = parseInt(card.getAttribute('data-total') || '0', 10) || 0;
      const el = card.querySelector('.card-progress');
      if (!el || !key) return;
      const state = loadState(key);
      const done = Object.keys(state).filter((k) => k !== '_updated' && state[k] === true).length;
      el.textContent = done + '/' + total;
      if (total && done >= total) card.classList.add('is-complete');
    });

    qsa('form[data-checklist]').forEach(initForm);

    qsa('[data-checklist-reset]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-storage-key');
        if (!key) return;
        if (!confirm('Reset all checks for this block on this browser?')) return;
        localStorage.removeItem(key);
        const form = qs('form[data-storage-key="' + key + '"]');
        if (!form) return location.reload();
        qsa('input[type="checkbox"][data-check-id]', form).forEach((input) => {
          input.checked = false;
          applyItemState(input);
        });
        updateProgress(form);
      });
    });

    qsa('[data-checklist-expand]').forEach((btn) => {
      btn.addEventListener('click', () => {
        qsa('.check-detail').forEach((el) => { el.style.display = ''; });
      });
    });
    qsa('[data-checklist-collapse]').forEach((btn) => {
      btn.addEventListener('click', () => {
        qsa('.check-detail').forEach((el) => { el.style.display = 'none'; });
      });
    });
  });
})();
