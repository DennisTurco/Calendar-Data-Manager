/**
 * Reads URL query parameters and pre-fills matching form fields on page load.
 * Supports: text inputs, textareas, selects, checkboxes.
 *
 * Example URLs:
 *   /new-events?summary=Work&date_from=2024-01-01T09:00&color=Blue
 *   /get-events?summary=Meeting&date_from=2024-01-01T00:00&date_to=2024-12-31T23:59
 */
document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    if (!params.toString()) return;

    params.forEach(function (value, key) {
        // Handle checkboxes by name
        const checkboxes = document.querySelectorAll(`input[type="checkbox"][name="${key}"]`);
        if (checkboxes.length > 0) {
            checkboxes.forEach(cb => {
                cb.checked = (value === 'true' || value === '1' || value === 'on');
            });
            return;
        }

        const el = document.querySelector(`[name="${key}"]`);
        if (!el) return;

        if (el.tagName === 'SELECT') {
            const opt = Array.from(el.options).find(o => o.value === value);
            if (opt) {
                opt.selected = true;
                // Mark so default_timezone.js does not override
                el.dataset.preserveValue = 'true';
            }
        } else {
            el.value = value;
        }
    });
});
