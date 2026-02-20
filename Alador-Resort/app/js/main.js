// 🚀 INIT SECTION
import { initNavbar } from "./navbar.js";
import { initCarousel } from "./carousel.js";
import { initLightbox } from "./lightbox.js";
import { initParallax } from "./parallax.js";
import { initFadeIns } from "./fadein.js";
import { initCounters } from "./counters.js";

document.addEventListener("DOMContentLoaded", () => {
  try {
    initNavbar();
    initCarousel();
    initLightbox();
    initParallax();
    initFadeIns();
    initCounters();
  } catch (error) {
    console.error("Init error:", error);
  }
});

const flatpickrOptions = {
  minDate: "today",
  dateFormat: "Y-m-d",
};
flatpickr("#checkin", flatpickrOptions);
flatpickr("#checkout", flatpickrOptions);

// 🍞 Toast Feedback
function showToast(message = "Booking confirmed!") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  toast.setAttribute("role", "alert");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

// 🖼️ Lightbox Behavior
function openLightbox(img) {
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  if (img?.src) {
    lightboxImg.src = img.src;
    lightbox.style.display = "flex";
    document.addEventListener("keydown", escClose);
  }
}

function closeLightbox() {
  document.getElementById("lightbox").style.display = "none";
  document.removeEventListener("keydown", escClose);
}

function escClose(e) {
  if (e.key === "Escape") closeLightbox();
}

// Initialize Leaflet Map
const map = L.map('map').setView([9.03, 38.74], 13); // Centered on Addis Ababa

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Optional: Add marker
L.marker([9.03, 38.74]).addTo(map)
  .bindPopup('Your location')
  .openPopup();

// Initialize QR Scanner
const qrScanner = new Html5QrcodeScanner(
  "qr-reader",
  {
    fps: 10,
    qrbox: { width: 250, height: 250 },
    aspectRatio: 1.0
  }
);

qrScanner.render(
  (decodedText) => {
    console.log("QR Code Scanned:", decodedText);
    alert("Scanned: " + decodedText);
  },
  (errorMessage) => {
    console.warn("QR Code scan error:", errorMessage);
  }
);