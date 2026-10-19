// Shared UI behaviour: theme toggle, sidebar, toasts, modals, clipboard, form loading states.
(function () {
    'use strict';

    /* ---------- Theme toggle ---------- */
    document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
        btn.addEventListener('click', () => window.toggleDarkMode());
    });

    /* ---------- Sidebar (mobile off-canvas) ---------- */
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    function setSidebar(open) {
        if (!sidebar) return;
        sidebar.classList.toggle('-translate-x-full', !open);
        overlay && overlay.classList.toggle('hidden', !open);
        document.querySelectorAll('[aria-controls="sidebar"]').forEach((b) => b.setAttribute('aria-expanded', String(open)));
        document.body.classList.toggle('overflow-hidden', open);
    }

    document.querySelectorAll('[data-sidebar-toggle]').forEach((el) => {
        el.addEventListener('click', () => setSidebar(sidebar.classList.contains('-translate-x-full')));
    });

    /* ---------- Toasts ---------- */
    const ICONS = {
        success: '<path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z"/><path d="m9 12 2 2 4-4"/>',
        error: '<circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
        info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    };

    function toastRegion() {
        let region = document.getElementById('toastRegion');
        if (!region) {
            region = document.createElement('div');
            region.id = 'toastRegion';
            region.className = 'toast-region';
            region.setAttribute('aria-live', 'polite');
            document.body.appendChild(region);
        }
        return region;
    }

    function dismissToast(el) {
        if (!el || el.classList.contains('is-leaving')) return;
        el.classList.add('is-leaving');
        setTimeout(() => el.remove(), 200);
    }

    function armToast(el) {
        const close = el.querySelector('[data-toast-close]');
        close && close.addEventListener('click', () => dismissToast(el));
        const timeout = el.classList.contains('toast-error') ? 8000 : 4500;
        let timer = setTimeout(() => dismissToast(el), timeout);
        el.addEventListener('mouseenter', () => clearTimeout(timer));
        el.addEventListener('mouseleave', () => { timer = setTimeout(() => dismissToast(el), 2000); });
    }

    window.showToast = function (message, type = 'success') {
        const el = document.createElement('div');
        el.className = `toast toast-${type}`;
        el.setAttribute('role', type === 'error' ? 'alert' : 'status');
        el.innerHTML = `
            <svg class="toast-icon w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[type] || ICONS.info}</svg>
            <span class="flex-1 pt-px"></span>
            <button type="button" class="btn btn-ghost btn-icon btn-sm -my-1" data-toast-close aria-label="Dismiss">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>`;
        el.querySelector('span').textContent = message;
        toastRegion().appendChild(el);
        armToast(el);
    };

    document.querySelectorAll('[data-toast]').forEach(armToast);

    /* ---------- Modals ---------- */
    let lastFocused = null;

    window.openModal = function (id) {
        const modal = document.getElementById(id);
        if (!modal) return;
        lastFocused = document.activeElement;
        modal.hidden = false;
        document.body.classList.add('overflow-hidden');
        requestAnimationFrame(() => {
            modal.classList.add('is-open');
            const focusTarget = modal.querySelector('[autofocus]') || modal.querySelector('[data-modal-close]:not(.modal-backdrop)');
            focusTarget && focusTarget.focus();
        });
    };

    window.closeModal = function (id) {
        const modal = document.getElementById(id);
        if (!modal || modal.hidden) return;
        modal.classList.remove('is-open');
        document.body.classList.remove('overflow-hidden');
        setTimeout(() => { modal.hidden = true; }, 200);
        lastFocused && lastFocused.focus && lastFocused.focus();
    };

    document.addEventListener('click', (e) => {
        const opener = e.target.closest('[data-modal-open]');
        if (opener) { window.openModal(opener.dataset.modalOpen); return; }
        const closer = e.target.closest('[data-modal-close]');
        if (closer) { const modal = closer.closest('.modal'); modal && window.closeModal(modal.id); }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key !== 'Escape') return;
        document.querySelectorAll('.modal.is-open').forEach((m) => window.closeModal(m.id));
        if (sidebar && !sidebar.classList.contains('-translate-x-full') && window.innerWidth < 1024) setSidebar(false);
    });

    /* ---------- Clipboard ---------- */
    window.copyText = function (text, successMsg) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text)
                .then(() => window.showToast(successMsg || 'Copied to clipboard'))
                .catch(() => window.prompt('Copy this:', text));
        }
        window.prompt('Copy this:', text);
        return Promise.resolve();
    };

    // Buttons with data-share-form="<formId>" copy a link that pre-fills that form.
    document.querySelectorAll('[data-share-form]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const form = document.getElementById(btn.dataset.shareForm);
            if (!form) return;
            const params = new URLSearchParams();
            for (const [key, value] of new FormData(form).entries()) {
                if (key !== 'action' && value) params.set(key, value);
            }
            const url = window.location.origin + window.location.pathname + (params.toString() ? '?' + params : '');
            window.copyText(url, 'Shareable link copied');
        });
    });

    /* ---------- Form loading state ---------- */
    // Forms with [data-loading-form]: the clicked submit button shows a spinner and its
    // name/value is preserved (disabled buttons are not submitted).
    document.querySelectorAll('form[data-loading-form]').forEach((form) => {
        form.addEventListener('submit', (e) => {
            const btn = e.submitter;
            if (!btn) return;
            if (btn.name) {
                const hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.name = btn.name;
                hidden.value = btn.value;
                form.appendChild(hidden);
            }
            form.querySelectorAll('button[type="submit"]').forEach((b) => {
                b.dataset.originalHtml = b.innerHTML;
                b.disabled = true;
            });
            btn.innerHTML = `<span class="spinner" aria-hidden="true"></span> ${btn.dataset.loadingText || 'Working…'}`;

            // Optional placeholder that replaces previous results while the server works
            const skeleton = btn.dataset.skeleton && document.getElementById(btn.dataset.skeleton);
            if (skeleton) {
                document.querySelectorAll('[data-results]').forEach((el) => { el.hidden = true; });
                skeleton.hidden = false;
                skeleton.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    });

    // Restore buttons when the page comes back from the bfcache (browser "Back")
    window.addEventListener('pageshow', (e) => {
        if (!e.persisted) return;
        document.querySelectorAll('button[data-original-html]').forEach((b) => {
            b.innerHTML = b.dataset.originalHtml;
            b.disabled = false;
        });
    });

    /* ---------- Date range guard + quick presets ---------- */
    const from = document.getElementById('date_from');
    const to = document.getElementById('date_to');
    if (from && to) {
        const pad = (n) => String(n).padStart(2, '0');
        const fmt = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
        const startOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0);
        const endOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), 23, 59);

        function presetRange(key) {
            const now = new Date();
            const y = now.getFullYear(), m = now.getMonth();
            switch (key) {
                case 'today': return [startOfDay(now), endOfDay(now)];
                case 'week': {
                    const monday = new Date(y, m, now.getDate() - ((now.getDay() + 6) % 7));
                    return [startOfDay(monday), endOfDay(new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + 6))];
                }
                case 'month': return [new Date(y, m, 1), endOfDay(new Date(y, m + 1, 0))];
                case 'last30': return [startOfDay(new Date(y, m, now.getDate() - 29)), endOfDay(now)];
                case 'year': return [new Date(y, 0, 1), endOfDay(new Date(y, 11, 31))];
                case 'lastyear': return [new Date(y - 1, 0, 1), endOfDay(new Date(y - 1, 11, 31))];
            }
            return null;
        }

        const presetButtons = document.querySelectorAll('[data-preset]');
        const markPreset = () => {
            presetButtons.forEach((b) => {
                const r = presetRange(b.dataset.preset);
                b.setAttribute('aria-pressed', String(!!r && from.value === fmt(r[0]) && to.value === fmt(r[1])));
            });
        };

        const sync = () => {
            to.min = from.value || '';
            if (from.value && to.value && to.value < from.value) to.setCustomValidity('"To" must be after "From"');
            else to.setCustomValidity('');
            markPreset();
        };

        presetButtons.forEach((b) => b.addEventListener('click', () => {
            const r = presetRange(b.dataset.preset);
            if (!r) return;
            from.value = fmt(r[0]);
            to.value = fmt(r[1]);
            sync();
        }));

        from.addEventListener('change', sync);
        to.addEventListener('change', sync);
        from.addEventListener('input', sync);
        to.addEventListener('input', sync);
        sync();
    }

    /* ---------- Sortable tables ---------- */
    // <table data-sortable> with <th data-sort="text|num">; a cell may carry data-value for its sort key.
    document.querySelectorAll('table[data-sortable]').forEach((table) => {
        const tbody = table.tBodies[0];
        const headers = Array.from(table.querySelectorAll('th'));
        const collator = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });

        headers.forEach((th, col) => {
            if (!th.dataset.sort) return;
            const sortBy = () => {
                const dir = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
                headers.forEach((h) => h.removeAttribute('aria-sort'));
                th.setAttribute('aria-sort', dir);
                const key = (row) => { const c = row.cells[col]; return c.dataset.value ?? c.innerText.trim(); };
                const rows = Array.from(tbody.rows);
                rows.sort((a, b) => {
                    const r = th.dataset.sort === 'num' ? parseFloat(key(a)) - parseFloat(key(b)) : collator.compare(key(a), key(b));
                    return dir === 'ascending' ? r : -r;
                });
                rows.forEach((r) => tbody.appendChild(r));
            };
            th.addEventListener('click', sortBy);
            th.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sortBy(); } });
        });
    });
})();
