// Loaded in <head>: applies the saved/system theme before first paint.
(function () {
    const STORAGE_KEY = 'cdm-theme';
    const html = document.documentElement;

    function readSaved() {
        try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
    }

    function getTheme() {
        return readSaved() || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    }

    function applyTheme(theme) {
        html.classList.toggle('dark', theme === 'dark');
        // Keep the mobile browser bar in sync with the chosen theme, not only the OS one
        document.querySelectorAll('meta[name="theme-color"]').forEach((m) => {
            m.setAttribute('content', theme === 'dark' ? '#0c0e13' : '#f5f6f8');
        });
        document.dispatchEvent(new CustomEvent('cdm:themechange', { detail: { theme } }));
    }

    applyTheme(getTheme());

    // Follow the OS setting until the user picks a theme explicitly
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!readSaved()) applyTheme(e.matches ? 'dark' : 'light');
    });

    window.toggleDarkMode = function () {
        const next = html.classList.contains('dark') ? 'light' : 'dark';
        try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* storage unavailable */ }
        applyTheme(next);
    };
})();
