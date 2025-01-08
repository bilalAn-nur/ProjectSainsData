<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4">
    <div class="max-w-4xl mx-auto bg-white p-6 shadow-md rounded-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">
        Prediksi Kasus DBD Kota Bandung
      </h2>
      <form @submit.prevent="fetchPrediction" class="space-y-4">
        <div>
          <label for="kecamatan" class="block text-gray-700 font-medium mb-2"
            >Pilih Kecamatan:</label
          >
          <select
            v-model="selectedKecamatan"
            required
            class="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-3 py-2"
          >
            <option
              v-for="kecamatan in kecamatans"
              :key="kecamatan"
              :value="kecamatan"
            >
              {{ kecamatan }}
            </option>
          </select>
        </div>
        <div>
          <label for="steps" class="block text-gray-700 font-medium mb-2"
            >Jumlah Prediksi (Tahun):</label
          >
          <input
            type="number"
            v-model="steps"
            min="1"
            required
            class="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-3 py-2"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Prediksi
        </button>
      </form>
      <div class="chart-container mt-8 bg-gray-50 rounded-md p-4 shadow">
        <canvas id="Analysis"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from "chart.js";
import { getPrediction } from "../services/api";

export default {
  data() {
    return {
      selectedKecamatan: "",
      steps: 5, // Menggunakan jumlah tahun untuk prediksi
      kecamatans: [], // Dinamis berdasarkan data dari API
      chart: null,
    };
  },
  async mounted() {
    // Ambil kecamatan dari API
    const response = await fetch("http://127.0.0.1:8000/data/");
    const data = await response.json();
    this.kecamatans = [...new Set(data.map((item) => item.bps_nama_kecamatan))];
  },
  methods: {
    async fetchPrediction() {
      try {
        const response = await getPrediction(
          this.selectedKecamatan,
          this.steps
        );
        const labels = Array.from(
          { length: this.steps },
          (_, i) => `Tahun ${2023 + i}`
        ); // Tahun 2023 untuk contoh
        const data = response.predictions;

        if (this.chart) this.chart.destroy();

        this.chart = new Chart(document.getElementById("Analysis"), {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: `Prediksi Kasus (${this.selectedKecamatan})`,
                data: data,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      } catch (error) {
        console.error("Error fetching prediction:", error);
        alert("Gagal memuat prediksi. Silakan coba lagi.");
      }
    },
  },
};
</script>
<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
  position: relative;
}
canvas {
  width: 100%;
  height: 100%;
}
</style>
