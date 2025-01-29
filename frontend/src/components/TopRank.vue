<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4">
    <div class="max-w-4xl mx-auto bg-white p-6 shadow-md rounded-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">
        DBD Kota Bandung - 3 Kecamatan dengan kasus tertinggi tahun
        {{ selectedYear ? selectedYear : "-" }}
      </h2>
      <form @submit.prevent="fetchData" class="space-y-4">
        <div>
          <label for="tahun" class="block text-gray-700 font-medium mb-2">
            Pilih Tahun
          </label>
          <select
            v-model="selectedYear"
            required
            class="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-3 py-2"
          >
            <option v-for="tahun in availableYears" :key="tahun" :value="tahun">
              {{ tahun }}
            </option>
          </select>
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Tampilkan Peringkat
        </button>
      </form>

      <div v-if="rankings.length" class="mt-8">
        <h3 class="text-xl font-bold text-gray-800 mb-4">
          Tahun {{ selectedYear }}
        </h3>
        <div class="flex justify-center items-end space-x-4">
          <!-- Juara 2 -->
          <div v-if="rankings[1]" class="flex flex-col items-center">
            <div
              class="w-24 h-40 flex items-end justify-center rounded-t-md shadow-md"
              style="background-color: #ffff00"
            >
              #2
            </div>
            <div class="text-center mt-2">
              <span class="font-medium">{{ rankings[1].kecamatan }}</span
              ><br />
              <span class="text-gray-600">{{ rankings[1].total }} Orang</span>
            </div>
          </div>

          <!-- Juara 1 -->
          <div v-if="rankings[0]" class="flex flex-col items-center">
            <div
              class="w-28 h-48 flex items-end justify-center rounded-t-md shadow-md"
              style="background-color: #ff0000"
            >
              #1
            </div>
            <div class="text-center mt-2">
              <span class="font-medium">{{ rankings[0].kecamatan }}</span
              ><br />
              <span class="text-gray-600">{{ rankings[0].total }} Orang</span>
            </div>
          </div>

          <!-- Juara 3 -->
          <div v-if="rankings[2]" class="flex flex-col items-center">
            <div
              class="w-24 h-32 flex items-end justify-center rounded-t-md shadow-md"
              style="background-color: #00ff00"
            >
              #3
            </div>
            <div class="text-center mt-2">
              <span class="font-medium">{{ rankings[2].kecamatan }}</span
              ><br />
              <span class="text-gray-600">{{ rankings[2].total }} Orang</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedYear: "",
      availableYears: [],
      rankings: [],
    };
  },
  async mounted() {
    // Ambil data tahun dari API
    const response = await fetch(
      "https://project-sains-data-backend.vercel.app/data/"
    );
    const data = await response.json();
    this.availableYears = [...new Set(data.map((item) => item.tahun))].sort();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(
          `https://project-sains-data-backend.vercel.app/data/?tahun=${this.selectedYear}`
        );
        const data = await response.json();

        // Filter data berdasarkan tahun yang dipilih
        const filteredData = data.filter(
          (item) => item.tahun === this.selectedYear
        );

        // Hitung total kasus per kecamatan untuk tahun yang dipilih
        const groupedData = filteredData.reduce((acc, item) => {
          if (!acc[item.bps_nama_kecamatan]) {
            acc[item.bps_nama_kecamatan] = 0;
          }
          acc[item.bps_nama_kecamatan] += item.total_kasus;
          return acc;
        }, {});

        // Ubah menjadi array dan urutkan berdasarkan total kasus
        this.rankings = Object.entries(groupedData)
          .map(([kecamatan, total]) => ({ kecamatan, total }))
          .sort((a, b) => b.total - a.total);
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Gagal memuat data. Silakan coba lagi.");
      }
    },
  },
};
</script>

<style scoped></style>
