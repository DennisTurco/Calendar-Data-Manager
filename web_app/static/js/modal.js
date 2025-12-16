function openModal(id) {
    const modal = document.getElementById(id);
    const panel = document.getElementById(id + "_panel");

    if (!modal || !panel) return;

    modal.classList.remove("hidden");

    requestAnimationFrame(() => {
        panel.classList.remove("scale-95", "opacity-0");
    });
}

function closeModal(id) {
    const modal = document.getElementById(id);
    const panel = document.getElementById(id + "_panel");

    if (!modal || !panel) return;

    panel.classList.add("scale-95", "opacity-0");

    setTimeout(() => {
        modal.classList.add("hidden");
    }, 200);
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        document.querySelectorAll("[id$='_panel']").forEach(panel => {
            const id = panel.id.replace("_panel", "");
            closeModal(id);
        });
    }
});
