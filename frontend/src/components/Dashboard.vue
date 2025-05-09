<template>
  <div>
    <h2>Dashboard Crédit Scoring</h2>
    <!-- Champ d'entrée modifié pour accepter des chaînes -->
    <input v-model="clientId" type="text" placeholder="Enter Client ID" />
    <button @click="fetchClientData">Submit</button>

    <div v-if="clientInfo">
      <h3>Informations Client</h3>
      <p>{{ clientInfo }}</p>
    </div>

    <div v-if="clientScore">
      <h3>Score Client</h3>
      <p>Score: {{ clientScore.score }}</p>
      <p>Interpretation: {{ clientScore.interpretation }}</p>
    </div>

    <div v-if="comparisonData">
      <h3>Comparaison avec d'autres clients</h3>
      <ul>
        <li v-for="client in comparisonData.similar_clients" :key="client.client_id">
          Client ID: {{ client.client_id }}, Income: {{ client.income }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      clientId: '', // Initialisé comme une chaîne vide
      clientInfo: null,
      clientScore: null,
      comparisonData: null,
    };
  },
  methods: {
    async fetchClientData() {
      // Validation de l'ID pour s'assurer qu'il est un entier positif
      const id = parseInt(this.clientId, 10);
      if (isNaN(id) || id <= 0) {
        alert("Please enter a valid Client ID (positive integer)");
        return;
      }

      try {
        const clientDataResponse = await axios.get(`http://127.0.0.1:5007/client_data?client_id=${id}`);
        const clientScoreResponse = await axios.get(`http://127.0.0.1:5007/client_score?client_id=${id}`);
        const comparisonResponse = await axios.get(`http://127.0.0.1:5007/compare_clients?client_id=${id}`);

        this.clientInfo = `Client ID: ${clientDataResponse.data.client_id}, Age: ${clientDataResponse.data.age}, Income: ${clientDataResponse.data.income}, Loan Amount: ${clientDataResponse.data.loan_amount}, Status: ${clientDataResponse.data.loan_status}`;
        this.clientScore = clientScoreResponse.data;
        this.comparisonData = comparisonResponse.data;
      } catch (error) {
        console.error("Error fetching client data:", error);
      }
    },
  },
};
</script>

<style>
/* Ajoutez ici vos styles pour le dashboard */
</style>
