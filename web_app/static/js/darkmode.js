(function () {
    const STORAGE_KEY = 'cdm-theme';
    const html = document.documentElement;

    const moonSVG = `<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>`;
    const sunSVG = `<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>`;

    function getTheme() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) return saved;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        html.classList.toggle('dark', theme === 'dark');
    }

    function updateBtn() {
        const btn = document.getElementById('darkModeToggle');
        if (!btn) return;
        const isDark = html.classList.contains('dark');
        btn.innerHTML = isDark ? sunSVG : moonSVG;
        btn.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
        btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    }

    // Apply immediately (before DOMContentLoaded) to avoid flash of wrong theme
    applyTheme(getTheme());

    window.toggleDarkMode = function () {
        const next = html.classList.contains('dark') ? 'light' : 'dark';
        localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
        updateBtn();
    };

    document.addEventListener('DOMContentLoaded', updateBtn);
})();
