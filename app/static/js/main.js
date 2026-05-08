// TaskOrbit — main.js
// Small UI helpers to improve the user experience

document.addEventListener("DOMContentLoaded", function () {

  // --- Auto-dismiss flash alerts after 4 seconds ---
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      // Use Bootstrap's dismiss method if available
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });

  // --- Add active class to current nav link ---
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach(function (link) {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
      link.style.color = "#e6edf3";
    }
  });

});
