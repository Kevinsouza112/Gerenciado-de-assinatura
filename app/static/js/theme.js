(() => {
  const root = document.documentElement;
  const storageKey = "subscription-theme";

  const preferredTheme = () => (
    window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
  );

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    const icon = document.getElementById("theme-toggle-icon");
    if (icon) {
      icon.className = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
    }
  };

  applyTheme(localStorage.getItem(storageKey) || preferredTheme());

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("theme-toggle");
    if (!button) {
      return;
    }

    button.addEventListener("click", () => {
      const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
      localStorage.setItem(storageKey, nextTheme);
      applyTheme(nextTheme);
    });
  });
})();
