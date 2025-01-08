import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../components/Dashboard.vue";
import Analysis from "../components/Analysis.vue";
import ManageData from "../components/ManageData.vue";
import Education from "../components/Education.vue";

const routes = [
  { path: "/", component: Dashboard },
  { path: "/analysis", component: Analysis },
  { path: "/manage-data", component: ManageData },
  { path: "/education", component: Education },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
