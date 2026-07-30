// Course site — small helpers
document.addEventListener('DOMContentLoaded', () => {
  const path = location.pathname.replace(/\\/g, '/');
  document.querySelectorAll('.nav a').forEach((a) => {
    const href = a.getAttribute('href');
    if (!href) return;
    const norm = href.replace(/^\.\.\//, '/site/').replace(/^\.\//, '');
    if (path.endsWith(href.replace('../', '').replace('./', '')) || path.endsWith(href)) {
      a.setAttribute('aria-current', 'page');
    }
  });
});
