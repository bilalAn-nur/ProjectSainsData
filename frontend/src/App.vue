<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-blue-600 text-white shadow-md">
      <div
        class="container mx-auto px-4 flex items-center justify-between py-4"
      >
        <h1 class="text-2xl font-bold">DBD Dashboard</h1>
        <nav class="hidden md:block">
          <ul class="flex space-x-6">
            <li>
              <router-link to="/" class="hover:underline"
                >Dashboard</router-link
              >
            </li>
            <li>
              <router-link to="/toprank" class="hover:underline"
                >Top Rank</router-link
              >
            </li>
            <li>
              <router-link to="/penyebaran" class="hover:underline"
                >Penyebaran</router-link
              >
            </li>
          </ul>
        </nav>
        <button
          @click="toggleMenu"
          class="md:hidden flex items-center text-white focus:outline-none"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        </button>
      </div>
      <!-- Dropdown menu for mobile -->
      <div v-if="isMenuOpen" class="md:hidden bg-blue-700">
        <ul class="flex flex-col space-y-2 py-2 px-4">
          <li>
            <router-link to="/" class="block hover:underline"
              >Dashboard</router-link
            >
          </li>
          <li>
            <router-link to="/analysis" class="block hover:underline"
              >Analysis</router-link
            >
          </li>
          <li>
            <router-link to="/manage-data" class="block hover:underline"
              >Manajemen Data</router-link
            >
          </li>
          <li>
            <router-link to="/education" class="block hover:underline"
              >Edukasi</router-link
            >
          </li>
        </ul>
      </div>
    </header>
    <main class="container mx-auto px-4 py-6">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
  },
};
</script>

<!-- <style>
@tailwind base;
@tailwind components;
@tailwind utilities;
</style> -->
