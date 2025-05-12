<template>
  <div class="score-chart">
    <div v-if="chartData" class="chart-container">
      <canvas ref="chartCanvas"></canvas>
      <!-- Affichage du score au centre de la jauge avec une couleur dynamique -->
      <div class="score-display" :style="{ color: scoreColor }">
        <p><strong>{{ Math.round(proba * 100) }}%</strong></p>
      </div>
    </div>
    <p v-else>Aucune donnée disponible pour le score.</p>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

// Enregistrez tous les modules nécessaires de Chart.js
Chart.register(...registerables);

export default {
  props: {
    proba: {
      type: Number,
      required: true,
    },
    chartData: {
      type: Object,
      required: true,
    },
    options: {
      type: Object,
      required: true,
    },
    classifications: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  computed: {
    scoreColor() {
      // Trouver la couleur correspondant à la probabilité
      const classification = this.classifications.find(
        (c) => this.proba * 100 >= c.min && this.proba * 100 <= c.max
      );
      return classification ? classification.color : '#333'; // Couleur par défaut
    },
    dynamicChartData() {
      // Mise à jour dynamique des couleurs de remplissage de la jauge
      return {
        ...this.chartData,
        datasets: [
          {
            ...this.chartData.datasets[0],
            backgroundColor: [this.scoreColor, '#f0f0f0'], // Gris plus pâle pour le restant
          },
        ],
      };
    },
  },
  watch: {
    proba: "renderChart",
    chartData: "renderChart",
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      if (this.chart) {
        this.chart.destroy();
      }

      const ctx = this.$refs.chartCanvas.getContext("2d");
      this.chart = new Chart(ctx, {
        type: "doughnut",
        data: this.dynamicChartData, // Utilisation des données dynamiques
        options: {
          ...this.options,
          plugins: {
            tooltip: { enabled: false },
            legend: { display: false },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.score-chart {
  max-width: 500px; /* Augmente la largeur maximale de la jauge */
  margin: 0 auto;
  text-align: center;
  position: relative;
}

.chart-container {
  position: relative;
  width: 100%;
  height: auto;
}

canvas {
  max-width: 100%;
  height: auto;
}

.score-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 4rem; /* Taille de la police encore plus grande */
  font-weight: 900; /* Mise en gras maximale */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3); /* Ajout d'une ombre pour accentuer */
}
</style>
