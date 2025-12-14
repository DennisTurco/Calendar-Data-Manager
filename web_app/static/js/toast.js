setTimeout(() => {
document
    .querySelectorAll('[data-toast]')
    .forEach(el => el.remove());
}, 4000);
