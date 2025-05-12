<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
    <div v-if="chartData.datasets[0]?.data[0]" class="score-display" :style="{ color: scoreColor }">
      <p style="font-size: 3rem; font-weight: 900;">{{ chartData.datasets[0].data[0] }}%</p> <!-- Police agrandie et gras forcé -->
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref, watch, computed } from 'vue';
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js';

Chart.register(DoughnutController, ArcElement, Tooltip, Legend);

export default defineComponent({
  props: {
    chartData: {
      type: Object,
      required: true,
      default: () => ({
        labels: [],
        datasets: []
      })
    },
    options: {
      type: Object,
      default: () => ({
        cutout: '70%', // Une forme bien ronde avec un gros trou au centre
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: false
          }
        }
      })
    },
    classifications: {
      type: Array,
      required: true,
      default: () => [] // Default to an empty array to avoid runtime errors
    }
  },
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null;

    // Calculer dynamiquement la couleur du score en fonction des classes
    const scoreColor = computed(() => {
      const score = props.chartData.datasets[0]?.data[0] || 0;
      if (!props.classifications || props.classifications.length === 0) {
        console.warn("Classifications are missing or empty.");
        return '#000000'; // Noir par défaut
      }
      const classification = props.classifications.find(
        (c) => score >= c.min && score <= c.max
      );
      if (!classification) {
        console.warn(`No classification found for score: ${score}`);
        return '#000000'; // Noir par défaut
      }
      return classification.color;
    });

    onMounted(() => {
      if (chartCanvas.value) {
        chartInstance = new Chart(chartCanvas.value, {
          type: 'doughnut',
          data: props.chartData,
          options: props.options
        });
      }
    });

    watch(() => props.chartData, (newData) => {
      if (chartInstance) {
        chartInstance.data = newData;
        chartInstance.update();
      }
    });

    return {
      chartCanvas,
      scoreColor
    };
  }
});
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: auto;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

.score-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem; /* Taille par défaut */
  font-weight: 900; /* Gras forcé */
  pointer-events: none;
  text-align: center;
}

/* Arrondir les angles des barres */
.bar {
  border-radius: 10px; /* Rayon pour arrondir les angles */
}
</style>
