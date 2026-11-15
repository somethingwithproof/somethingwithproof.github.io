// Loaded in <head> so a saved theme applies before first paint.
(() => {
  const root = document.documentElement;
  try {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  } catch { /* storage blocked: follow the system setting */ }

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("[data-theme-toggle]");
    if (!button) return;
    const current = () => root.dataset.theme
      || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const label = () => button.setAttribute("aria-label",
      current() === "dark" ? "Switch to light theme" : "Switch to dark theme");
    label();
    button.addEventListener("click", () => {
      const next = current() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch { /* not persisted */ }
      label();
    });
  });
})();
