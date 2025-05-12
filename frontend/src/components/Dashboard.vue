<template>
  <div class="dashboard">
    <h2><strong>Dashboard Crédit Scoring</strong></h2> <!-- Titre en gras -->
    <!-- Champ d'entrée pour l'ID client -->
    <input v-model="clientId" type="text" placeholder="Entrez l'ID du client" />
    <button @click="fetchClientData">Soumettre</button>

    <!-- Affichage des informations du client -->
    <div v-if="clientData">
      <h3><strong>Informations du client</strong></h3> <!-- Titre en gras -->
      <p><strong>ID Client :</strong> {{ clientData.sk_id_curr }}</p>
      <p><strong>Genre :</strong> {{ clientData.client_info.gender }}</p>
      <p><strong>Montant du crédit :</strong> {{ clientData.client_info.credit_amount }} €</p>
      <p><strong>Prix des biens :</strong> {{ clientData.client_info.goods_price }} €</p>
      <p><strong>Années d'emploi :</strong> {{ clientData.client_info.employment_years }}</p>
      <p><strong>Nombre de membres de la famille :</strong> {{ clientData.client_info.family_members }}</p>
      <p><strong>Nombre d'enfants :</strong> {{ clientData.client_info.children_count }}</p>
      <p><strong>Évaluation de la région :</strong> {{ clientData.client_info.region_rating }}</p>
    </div>

    <!-- Affichage du score et de la probabilité -->
    <div v-if="clientData">
      <h3><strong>Score et Probabilité</strong></h3> <!-- Titre en gras -->
      <p><strong>Prédiction :</strong> {{ clientData.prediction }}</p>
      <p><strong>Probabilité :</strong> {{ (clientData.proba * 100).toFixed(2) }}%</p>
    </div>

    <!-- Affichage des features utilisées par le modèle -->
    <div v-if="clientData">
      <h3><strong>Features utilisées par le modèle</strong></h3> <!-- Titre en gras -->
      <ul>
        <li v-for="(value, key) in clientData.model_features" :key="key">
          <strong>{{ key }} :</strong> {{ value }}
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
      clientId: '', // ID du client saisi par l'utilisateur
      clientData: null, // Données du client récupérées depuis l'API
    };
  },
  methods: {
    async fetchClientData() {
      if (!this.clientId) {
        alert("Veuillez entrer un ID client valide.");
        return;
      }

      try {
        // Suppression du préfixe `api` dans l'URL
        const response = await axios.get(`http://127.0.0.1:5007/predict/${this.clientId}`);
        this.clientData = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
        alert("Impossible de récupérer les données pour cet ID client.");
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

input {
  width: calc(100% - 20px);
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background-color: #ff0000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #cc0000;
}

h3 {
  margin-top: 20px;
  color: #333;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 5px;
}
</style>
