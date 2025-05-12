import './assets/main.css';
import '@fortawesome/fontawesome-free/css/all.css'; // Importation de Font Awesome

import { createApp } from 'vue';
import App from './App.vue';
import CanvasJSChart from '@canvasjs/vue-charts';
import router from './router'; // Importation du routeur

const app = createApp(App);

// Enregistrement global du composant CanvasJSChart
app.component('CanvasJSChart', CanvasJSChart);

app.use(router); // Utilisation du routeur
app.mount('#app');
