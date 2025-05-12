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
          <h2>Informations du client</h2>
          <div class="client-info-cards">
            <div class="info-card">
              <i class="fas fa-id-card"></i>
              <p>{{ client.SK_ID_CURR }}</p>
            </div>
            <div class="info-card">
              <i class="fas fa-user"></i>
              <p>{{ client.CODE_GENDER }}</p>
            </div>
            <div class="info-card">
              <i class="fas fa-heart"></i>
              <p>{{ client.NAME_FAMILY_STATUS }}</p>
            </div>
            <div class="info-card">
              <span>Revenu</span>
              <p>{{ client.AMT_INCOME_TOTAL }} €</p>
            </div>
            <div class="info-card">
              <i class="fas fa-credit-card"></i>
              <p>{{ client.AMT_CREDIT }} €</p>
            </div>
          </div>
        </section>
        <p v-else>Chargement des données client...</p>

        <section v-if="score !== null && chartData !== null" class="score-section">
          <div class="visual-container">
            <div class="chart-container">
              <ScoreChart :chartData="chartData" :options="chartOptions" :classifications="classifications" />
            </div>
            <div class="classification-container">
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
import ScoreChart from '../components/ScoreChart.vue'; // Importation du composant ScoreChart

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

const fetchClientData = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/client/${clientId}`);
    if (response.data && response.data.length > 0) {
      client.value = response.data[0];
    } else {
      client.value = null;
      alert("Client introuvable. Veuillez vérifier l'ID.");
      router.push("/");
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des données client :", error);
  }
};

const fetchClientScore = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/predict/${clientId}`);
    score.value = response.data.score;

    chartData.value = {
      labels: ['Score obtenu', 'Restant'],
      datasets: [
        {
          data: [score.value, 100 - score.value],
          backgroundColor: [gaugeFillColor.value, '#E8E8E8'], // Utilisation de gaugeFillColor
          borderWidth: 0
        }
      ]
    };
  } catch (error) {
    console.error("Erreur lors de la récupération du score :", error);
    score.value = null;
    chartData.value = null;
  }
};

onMounted(async () => {
  await fetchClientData();
  await fetchClientScore();
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
  justify-content: center; /* Centre horizontalement */
  align-items: center; /* Centre verticalement */
  min-height: 100vh;
  background-color: var(--primary-color); /* Fond rouge */
  padding: 20px;
  box-sizing: border-box;
}

.dashboard {
  width: 100%;
  max-width: 1200px; /* Limite la largeur maximale */
  background-color: var(--secondary-color); /* Fond blanc pour contraste */
  color: var(--text-color);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header {
  background-color: var(--secondary-color); /* Fond blanc pour contraste */
  color: var(--primary-color); /* Texte rouge */
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
  margin-bottom: 30px;
}

.client-info-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 15px;
  justify-content: space-between;
}

.info-card {
  background-color: var(--secondary-color); /* Fond blanc pour contraste */
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
  margin-top: 20px;
}

.visual-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 300px;
  height: 300px;
}

.classification-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.classification-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  white-space: nowrap;
}

.range {
  width: 80px;
  text-align: right;
  margin-right: 10px;
  font-size: 0.9rem;
  font-weight: bold;
}

.bar {
  width: 100px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: relative;
}

.letter {
  color: white;
  font-size: 1rem;
  font-weight: bold;
  margin-left: 5px;
}

.footer {
  background-color: var(--secondary-color); /* Fond blanc pour contraste */
  color: var(--primary-color); /* Texte rouge */
  text-align: center;
  padding: 10px;
  margin-top: 40px;
}
</style>
