<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4">
    <div class="max-w-6xl mx-auto bg-white p-6 shadow-md rounded-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">
        Peta Persebaran DBD di Kota Bandung
      </h2>
      <div class="mb-4 text-center">
        <label for="year" class="mr-2">Pilih Tahun:</label>
        <select v-model="selectedYear" @change="fetchData">
          class="p-2 border rounded" >
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>
      <div id="map" class="w-full h-96"></div>
      <div id="legend" class="mt-4 flex justify-center items-center space-x-4">
        <div class="flex items-center">
          <span
            class="inline-block w-4 h-4 rounded-full bg-red-500 mr-2"
          ></span>
          <span>Zona Merah (> 200 kasus)</span>
        </div>
        <div class="flex items-center">
          <span
            class="inline-block w-4 h-4 rounded-full bg-yellow-400 mr-2"
          ></span>
          <span>Zona Kuning (51-200 kasus)</span>
        </div>
        <div class="flex items-center">
          <span
            class="inline-block w-4 h-4 rounded-full bg-green-500 mr-2"
          ></span>
          <span>Zona Hijau (0-50 kasus)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default {
  data() {
    return {
      map: null,
      geojson: null,
      casesData: {},
      selectedYear: null,
      availableYears: [],
    };
  },
  async mounted() {
    this.initMap();
    const response = await fetch(
      `https://project-sains-data-backend.vercel.app/data/`
    );
    const data = await response.json();

    if (data.length > 0) {
      this.availableYears = [...new Set(data.map((item) => item.tahun))].sort(
        (a, b) => b - a
      );
      this.selectedYear = this.availableYears[0]; // Pilih tahun pertama secara otomatis
      this.fetchData(); // Memuat data setelah tahun dipilih
    }
  },
  methods: {
    initMap() {
      this.map = L.map("map").setView([-6.9147, 107.6098], 12);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(
        this.map
      );
    },
    async fetchData() {
      try {
        if (!this.selectedYear) return; // Tidak memuat data jika tahun tidak dipilih

        const [geojsonResponse, casesResponse] = await Promise.all([
          fetch(
            "/geojson-bandung-master/3273-kota-bandung-level-kecamatan.json"
          ),
          fetch(`https://project-sains-data-backend.vercel.app/data/`),
        ]);

        const geojsonData = await geojsonResponse.json();
        const data = await casesResponse.json();

        // Filter data berdasarkan tahun yang dipilih
        const filteredData = data.filter(
          (item) => item.tahun === this.selectedYear
        );

        if (filteredData.length === 0) {
          alert("Data tidak tersedia untuk tahun ini!");
          return;
        }

        // Menyusun data kasus berdasarkan bps_kode_kecamatan
        this.casesData = filteredData.reduce((acc, item) => {
          acc[item.bps_kode_kecamatan] = item.total_kasus;
          return acc;
        }, {});

        // Jika sudah ada geojson sebelumnya, hapus dulu
        if (this.geojson) {
          this.map.removeLayer(this.geojson);
        }

        // Menampilkan geojson pada peta dengan styling dan popup
        this.geojson = L.geoJSON(geojsonData, {
          style: this.styleFeature,
          onEachFeature: this.onEachFeature,
        }).addTo(this.map);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    styleFeature(feature) {
      const idKecamatan = feature.properties.id_kecamatan;
      const cases = this.casesData[idKecamatan] || 0;

      const ranges = [
        { min: 200, max: Infinity, color: "#FF0000", label: "Merah" }, // Zona Merah
        { min: 51, max: 199, color: "#FFFF00", label: "Kuning" }, // Zona Kuning
        { min: 0, max: 50, color: "#00FF00", label: "Hijau" }, // Zona Hijau
      ];

      // Menentukan zona berdasarkan rentang jumlah kasus
      const zone = ranges.find(
        (range) => cases >= range.min && cases <= range.max
      );

      return {
        fillColor: zone ? zone.color : "#FFFFFF", // Default to white if no zone matched
        weight: 1,
        opacity: 1,
        color: "white",
        fillOpacity: 0.7,
      };
    },
    onEachFeature(feature, layer) {
      const idKecamatan = feature.properties.id_kecamatan;
      const cases = this.casesData[idKecamatan] || 0;

      layer.bindPopup(
        `<strong>${feature.properties.nama_kecamatan}</strong><br>Jumlah Kasus: ${cases}`
      );
    },
  },
};
</script>

<style scoped>
#map {
  height: 500px;
}
</style>
