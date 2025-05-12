<template>
  <div class="dashboard-container">
    <div class="dashboard">
      <!-- Haut de page -->
      <header class="header">
        <h1>Votre Score de Crédit</h1>
      </header>

      <!-- Contenu principal -->
      <main class="main-content">
        <section v-if="client" class="client-info-section">
          <h2><strong>Informations du client</strong></h2>
          <div class="client-info-cards">
            <div class="info-card">
              <i class="fas fa-id-card"></i>
              <p><strong>ID:</strong> {{ client.sk_id_curr }}</p>
            </div>
            <div class="info-card">
              <i class="fas fa-user"></i>
              <p><strong>Genre:</strong> {{ client.gender }}</p>
            </div>
            <div class="info-card">
              <i class="fas fa-heart"></i>
              <p><strong>Nombre de membres de la famille:</strong> {{ client.family_members }}</p>
            </div>
            <div class="info-card">
              <span><strong>Montant du bien:</strong></span>
              <p>{{ client.goods_price }} €</p>
            </div>
             <div class="info-card">
              <p><strong>Nombre d'enfants: <br> </strong> {{ client.children_count }}</p>
            </div>
            
            <div class="info-card">
              <i class="fas fa-briefcase"></i>
              <p><strong>Années d'emploi:</strong> {{ client.employment_years }} ans</p>
            </div>
           <div class="info-card">
              <i class="fas fa-credit-card"></i>
              <p><strong>Montant du crédit:</strong> {{ client.credit_amount }} €</p>
            </div>
          </div>
        </section>
        <p v-else>Chargement des données client...</p>

        <section v-if="score !== null && chartData !== null" class="score-section">
          <div class="visual-container">
            <div class="chart-container">
              <h3 class="visual-title"><strong>Score du Crédit</strong></h3>
              <ScoreChart :chartData="chartData" :options="chartOptions" :classifications="classifications" :proba="score" />
            </div>
            <div class="classification-container">
              <h3 class="visual-title"><strong>Votre Situation</strong></h3>
              <div class="classification-bar" v-for="classification in classifications" :key="classification.label">
                <span class="range">{{ classification.range }}</span>
                <div
                  class="bar"
                  :style="{ backgroundColor: classification.color, borderRadius: '10px' }"
                >
                  <span class="letter">{{ classification.label }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
        <p v-else>Chargement du score...</p>
      </main>

      <!-- Bas de page -->
      <footer class="footer">
        <p>&copy; 2025 HomeCredit. Tous droits réservés.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import ScoreChart from '../components/ScoreChart.vue'; // Assurez-vous que le chemin est correct

const route = useRoute();
const router = useRouter();
const clientId = route.params.id;

const client = ref(null);
const score = ref(null);
const chartData = ref(null);
const chartOptions = ref({
  cutout: '70%', // Taille du trou au centre
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false }
  }
});

const classifications = ref([
  { range: '1% - 21%', color: 'green', label: 'A', min: 1, max: 21 },
  { range: '22% - 34%', color: 'yellow', label: 'B', min: 22, max: 34 },
  { range: '35% - 51%', color: '#FFA500', label: 'C', min: 35, max: 51 },
  { range: '52% - 73%', color: '#FF6347', label: 'D', min: 52, max: 73 },
  { range: '74% - 100%', color: '#8B0000', label: 'E', min: 74, max: 100 }
]);

const gaugeFillColor = computed(() => {
  const classification = classifications.value.find(
    (c) => score.value >= c.min && score.value <= c.max
  );
  return classification ? classification.color : '#D3D3D3'; // Couleur par défaut si aucune correspondance
});

const fetchClientDataAndScore = async () => {
  try {
    // Mise à jour pour utiliser la route `/predict` qui retourne toutes les données nécessaires
    const response = await axios.get(`http://localhost:5007/predict/${clientId}`);
    const data = response.data;

    // Log des données retournées par l'API
    console.log("Données retournées par l'API :", data);

    // Mise à jour des informations du client
    client.value = {
      sk_id_curr: data.sk_id_curr,
      gender: data.client_info.gender,
      credit_amount: data.client_info.credit_amount,
      goods_price: data.client_info.goods_price,
      employment_years: data.client_info.employment_years,
      family_members: data.client_info.family_members,
      children_count: data.client_info.children_count,
      region_rating: data.client_info.region_rating,
      prediction: data.proba // Ajout de la prédiction
    };

    // Mise à jour du score et des données pour le graphique
    score.value = data.proba;
    chartData.value = {
      labels: ['Score obtenu', 'Restant'],
      datasets: [
        {
          data: [data.proba * 100, 100 - data.proba * 100],
          backgroundColor: [gaugeFillColor.value, '#E8E8E8'], // Utilisation de gaugeFillColor
          borderWidth: 0
        }
      ]
    };
  } catch (error) {
    console.error("Erreur lors de la récupération des données :", error);
    client.value = null;
    score.value = null;
    chartData.value = null;
    alert("Impossible de récupérer les données pour cet ID client.");
    router.push("/");
  }
};

onMounted(async () => {
  await fetchClientDataAndScore();
});
</script>

<style scoped>
/* Couleurs principales */
:root {
  --primary-color: #ff0000; /* Rouge */
  --secondary-color: #ffffff; /* Blanc */
  --text-color: #333333; /* Gris foncé */
}

.dashboard-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--primary-color);
  padding: 20px;
  box-sizing: border-box;
}

.dashboard {
  width: 100%;
  max-width: 1200px; /* Largeur maximale pour les écrans larges */
  background-color: var(--secondary-color);
  color: var(--text-color);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header {
  background-color: var(--secondary-color);
  color: var(--primary-color);
  padding: 20px;
  text-align: center;
}

.header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: bold;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.client-info-section {
  margin-bottom: 50px; /* Ajoute un espace sous les informations du client */
}

.client-info-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 15px;
  justify-content: space-between;
}

.info-card {
  background-color: var(--secondary-color);
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  padding: 15px;
  flex: 1 1 calc(30% - 15px); /* Ajuste la largeur des cartes */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.info-card i,
.info-card span {
  font-size: 1.5rem;
  color: var(--primary-color);
  margin-bottom: 10px;
  display: block;
  font-weight: bold;
}

.info-card p {
  margin: 0;
  font-size: 1rem;
  font-weight: bold;
}

.score-section {
  margin-top: 40px; /* Descend les visuels et leurs titres */
}

.visual-container {
  display: flex;
  justify-content: center; /* Centre les visuels horizontalement */
  align-items: center; /* Aligne les visuels verticalement */
  gap: 40px; /* Ajoute un espace entre les visuels */
  margin-top: 20px; /* Ajoute un espace au-dessus des visuels */
}

.chart-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 400px; /* Limite la largeur des visuels */
}

.classification-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end; /* Aligne le visuel des barres vers la droite */
  justify-content: flex-start; /* Descend les barres pour les aligner avec la jauge */
  margin-top: 50px; /* Ajoute un espace pour descendre les barres */
  text-align: right; /* Aligne le texte à droite */
  max-width: 400px; /* Limite la largeur des visuels */
}

.chart-container canvas {
  width: 450px !important; /* Augmente la largeur de la jauge */
  height: 450px !important; /* Augmente la hauteur de la jauge */
}

.visual-title {
  margin-bottom: 20px; /* Ajoute un espace entre le titre et le visuel */
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
}

.classification-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px; /* Restauration de l'espacement précédent */
  width: 100%; /* Les barres prennent toute la largeur */
  white-space: nowrap; /* Forcer l'affichage sur une seule ligne */
}

.range {
  width: 80px; /* Restauration de la largeur précédente des étiquettes */
  text-align: right;
  margin-right: 10px;
  font-size: 0.9rem; /* Restauration de la taille de la police précédente */
  font-weight: bold;
  white-space: nowrap; /* Empêche le retour à la ligne */
}

.bar {
  flex: 1;
  height: 20px; /* Restauration de la hauteur précédente des barres */
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: relative;
}

.letter {
  color: white;
  font-size: 1rem;
  font-weight: bold;
  margin-left: 5px; /* Restauration de l'espacement précédent */
}

.classification-container {
  max-width: 300px; /* Réduction de la largeur maximale des barres */
  margin: 0 auto;
}

.footer {
  background-color: var(--secondary-color);
  color: var(--primary-color);
  text-align: center;
  padding: 10px;
  margin-top: 40px;
}

/* Suppression de la responsivité */
@media (max-width: 768px) {
  .visual-container {
    flex-direction: row; /* Les visuels restent alignés horizontalement */
    justify-content: space-between;
  }

  .chart-container,
  .classification-container {
    flex: 1 1 45%; /* Les visuels conservent leur largeur */
    max-width: 600px;
  }

  .info-card {
    flex: 1 1 calc(30% - 15px); /* Les cartes conservent leur largeur */
  }
}
</style>
