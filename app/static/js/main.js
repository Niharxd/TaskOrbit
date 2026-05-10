// TaskOrbit — main.js

// ── Page fade-in ──
document.body.classList.add("loaded");

document.addEventListener("DOMContentLoaded", function () {

  // ── Auto-dismiss flash alerts after 4 seconds ──
  document.querySelectorAll(".alert").forEach(function (alert) {
    setTimeout(function () {
      bootstrap.Alert.getOrCreateInstance(alert).close();
    }, 4000);
  });

  // ── Highlight active nav link ──
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-link").forEach(function (link) {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });

  // ── WebSocket: real-time toast notifications ──
  // Only runs if Socket.IO client was loaded (i.e. user is logged in)
  if (typeof io !== "undefined") {
    const socket = io();

    socket.on("task_event", function (data) {
      showToast(data.message, data.type);
    });
  }

});


// Show a small toast notification at the bottom-right
function showToast(message, type) {
  const container = document.getElementById("toast-container");
  if (!container) return;

  // Pick icon based on event type
  const icons = {
    created: "bi-plus-circle-fill",
    updated: "bi-pencil-fill",
    deleted: "bi-trash3-fill",
  };
  const icon = icons[type] || "bi-info-circle-fill";

  const toastEl = document.createElement("div");
  toastEl.className = "to-toast";
  toastEl.innerHTML = `
    <i class="bi ${icon} me-2"></i>
    <span>${message}</span>
  `;

  container.appendChild(toastEl);

  // Trigger fade-in
  requestAnimationFrame(function () {
    toastEl.classList.add("show");
  });

  // Auto-remove after 3.5 seconds
  setTimeout(function () {
    toastEl.classList.remove("show");
    setTimeout(function () { toastEl.remove(); }, 400);
  }, 3500);
}
