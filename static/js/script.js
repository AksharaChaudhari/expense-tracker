// script.js - draws the category chart (Chart.js loaded from a CDN)
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("categoryChart");
    if (!canvas) return;

    // Load Chart.js only on pages that need it
    const lib = document.createElement("script");
    lib.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js";
    lib.onload = () => {
        new Chart(canvas, {
            type: "doughnut",
            data: {
                labels: JSON.parse(canvas.dataset.labels),
                datasets: [{ data: JSON.parse(canvas.dataset.values) }],
            },
            options: { plugins: { legend: { position: "bottom" } } },
        });
    };
    document.head.appendChild(lib);
});
