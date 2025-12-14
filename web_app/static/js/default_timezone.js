const browserTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

const timezoneSelect = document.getElementById('timezone');

if (timezoneSelect) {
    const option = Array.from(timezoneSelect.options).find(opt => opt.value === browserTimezone);
    if (option) {
        option.selected = true;
    }
}