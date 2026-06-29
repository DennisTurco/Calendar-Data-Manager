const browserTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

const timezoneSelect = document.getElementById('timezone');

// Only auto-detect if the server has not already pre-selected a value
// and there is no timezone specified in the URL query parameters
const _urlTimezone = new URLSearchParams(window.location.search).get('timezone');
if (timezoneSelect && !timezoneSelect.dataset.preserveValue && !_urlTimezone) {
    const option = Array.from(timezoneSelect.options).find(opt => opt.value === browserTimezone);
    if (option) {
        option.selected = true;
    }
}