// Minimal map initializer for the map_widget component
(function(){
  const el = document.getElementById('resort-map');
  if (!el || typeof L === 'undefined') return;
  const lat = 9.061245, lng = 38.866302;
  const map = L.map('resort-map').setView([lat, lng], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  L.marker([lat, lng]).addTo(map).bindPopup('Alador Resort').openPopup();
})();