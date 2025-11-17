document.addEventListener("DOMContentLoaded", function() {
  // Inizializza mappa
  var map = L.map(document.querySelector(".map-container"), { zoomControl: false }).setView([37.265072111776625, 14.690961105310981], 17);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  L.control.zoom({ position: 'bottomleft' }).addTo(map);

  // Icone categorie
  var categoryIcons = {
    "Servizi Pubblici": L.icon({iconUrl:"/static/assets/icons/servizi_pubblici.svg", iconSize:[32,32]}),
    "Servizi Culturali": L.icon({iconUrl:"/static/assets/icons/servizi_culturali.svg", iconSize:[32,32]}),
    "Prodotti Tipici": L.icon({iconUrl:"/static/assets/icons/prodotti_tipici.svg", iconSize:[32,32]}),
    "Ospitalità": L.icon({iconUrl:"/static/assets/icons/ospitalita.svg", iconSize:[32,32]}),
    "Luoghi Verghiani": L.icon({iconUrl:"/static/assets/icons/luoghi_verghiani.svg", iconSize:[32,32]}),
    "Ristorazione": L.icon({iconUrl:"/static/assets/icons/ristorazione.svg", iconSize:[32,32]})
  };

  var markers = [];
  var allPointsData = [];

  // Aggiungi marker
  mineoPoints.forEach(p => {
    allPointsData.push(p);
    if(!p.coords) return;

    // 🔵 LINK GRATUITO GOOGLE MAPS PER IL PERCORSO
    var routeLink = `https://www.google.com/maps/dir/?api=1&destination=${p.coords[0]},${p.coords[1]}`;

    // Marker + popup con link percorso
    var m = L.marker(p.coords, {icon: categoryIcons[p.type]})
             .bindPopup(`
                <strong>${p.name}</strong><br>
                ${p.type}<br><br>
                <a href="${routeLink}" target="_blank" style="color:#007bff; font-weight:bold;">
                  ➤ Ottieni percorso
                </a>
             `);

    m.type = p.type;
    m.name = p.name;
    markers.push(m);
    m.addTo(map);
  });

  // Filtri
  function filterMarkers(type){
    markers.forEach(m => {
      if(type === "all" || m.type === type){
        if(!map.hasLayer(m)) map.addLayer(m);
      } else {
        if(map.hasLayer(m)) map.removeLayer(m);
      }
    });
  }

  const dropdownBtn = document.querySelector(".filter-dropdown");
  const filterItems = document.querySelectorAll(".filter-item");
  const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(dropdownBtn);

  filterItems.forEach(item => {
    item.addEventListener("click", function(){
      const type = this.dataset.type;
      filterMarkers(type);

      filterItems.forEach(i => i.classList.remove("active"));
      this.classList.add("active");

      dropdownInstance.hide();
      dropdownBtn.innerHTML = `<i class="bi bi-funnel-fill fs-5"></i> ${this.textContent}`;
    });
  });

  // Ricerca live
  const searchBox = document.querySelector(".search-box");
  const searchResults = document.querySelector(".search-results");

  searchBox.addEventListener("input", function(){
    const q = this.value.toLowerCase().trim();
    searchResults.innerHTML = "";
    if(q.length < 2){
      searchResults.style.display = "none";
      return;
    }

    const filtered = allPointsData.filter(p => p.name.toLowerCase().includes(q));

    filtered.forEach(p => {
      const div = document.createElement("div");
      div.className = "search-result-item";
      div.textContent = p.name;
      div.addEventListener("click", function(){
        if(p.coords) map.setView(p.coords, 18);
        const m = markers.find(m => m.name === p.name);
        if(m) m.openPopup();

        searchBox.value = "";
        searchResults.style.display = "none";
      });
      searchResults.appendChild(div);
    });

    searchResults.style.display = filtered.length ? "block" : "none";
  });

  document.addEventListener("click", function(e){
    if(!e.target.closest(".search-container")){
      searchResults.style.display = "none";
    }
  });
});
