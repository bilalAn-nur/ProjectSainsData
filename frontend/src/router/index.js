import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../components/Dashboard.vue";
import TopRank from "../components/TopRank.vue";
import Penyebaran from "../components/Penyebaran.vue";

const routes = [
  { path: "/", component: Dashboard },
  { path: "/toprank", component: TopRank },
  { path: "/penyebaran", component: Penyebaran },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
