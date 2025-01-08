<template>
  <div>
    <h2 class="text-xl font-bold mb-4">Manajemen Data</h2>
    <table class="min-w-full bg-white border rounded-lg shadow">
      <thead>
        <tr class="bg-blue-600 text-white">
          <th class="py-2 px-4">Kecamatan</th>
          <th class="py-2 px-4">Jumlah Kasus</th>
          <th class="py-2 px-4">Tahun</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in data" :key="index" class="text-center">
          <td class="py-2 px-4">{{ item.bps_nama_kecamatan }}</td>
          <td class="py-2 px-4">{{ item.total_kasus }}</td>
          <td class="py-2 px-4">{{ item.tahun }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      data: [],
    };
  },
  async mounted() {
    const response = await axios.get("http://127.0.0.1:8000/data/");
    this.data = response.data;
  },
};
</script>
