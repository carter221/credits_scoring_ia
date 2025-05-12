import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '../views/DashboardView.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView
  }
  // Ajoutez d'autres routes ici si nécessaire
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
