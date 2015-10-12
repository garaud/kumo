
var map = L.map('map').setView([46., 0.], 5);

L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "<a href=\"www.openstreetmap.org/copyright\" target=\"blank\">© OpenStreetMap contributors</a>",
  maxZoom: 18,
  subdomains: "abc"
}).addTo(map);
