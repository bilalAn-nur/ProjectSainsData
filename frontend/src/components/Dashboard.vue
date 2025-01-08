<template>
  <div>
    <h2 class="text-xl font-bold mb-4">Dashboard</h2>
    <div class="mb-6">
      <canvas id="trendLine"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js"; // Mengimpor Chart.js
import axios from "axios";

Chart.register(...registerables); // Mendaftarkan semua elemen Chart.js

export default {
  async mounted() {
    // Mengambil data dari backend
    const response = await axios.get("http://127.0.0.1:8000/data/");
    const data = response.data;

    // Menyiapkan data untuk grafik
    const kecamatan = [...new Set(data.map((item) => item.bps_nama_kecamatan))];
    const datasets = kecamatan.map((kec) => {
      const kecData = data.filter((item) => item.bps_nama_kecamatan === kec);
      return {
        label: kec,
        data: kecData.map((item) => item.total_kasus),
        borderColor: this.getRandomColor(),
        fill: false,
      };
    });

    // Membuat grafik menggunakan Chart.js
    new Chart(document.getElementById("trendLine").getContext("2d"), {
      type: "line",
      data: {
        labels: [...new Set(data.map((item) => item.tahun))], // Mengambil label tahun dari data
        datasets: datasets, // Dataset yang telah disiapkan
      },
    });
  },
  methods: {
    // Fungsi untuk menghasilkan warna acak untuk setiap garis grafik
    getRandomColor() {
      return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
    },
  },
};
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: auto;
}
</style>
