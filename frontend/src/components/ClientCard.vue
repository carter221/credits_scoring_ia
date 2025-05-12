<template>
  <div class="client-card">
    <h2>Informations du client</h2>
    <ul v-if="client">
      <li><strong>ID:</strong> {{ client.SK_ID_CURR }}</li>
      <li><strong>Genre:</strong> {{ client.CODE_GENDER }}</li>
      <li><strong>Revenu:</strong> {{ client.AMT_INCOME_TOTAL }} €</li>
      <li><strong>Montant du crédit:</strong> {{ client.AMT_CREDIT }} €</li>
      <li><strong>Statut familial:</strong> {{ client.NAME_FAMILY_STATUS }}</li>
    </ul>
    <p v-else>
      Chargement des données client...
      <br />
      <strong>Debug:</strong> {{ client }}
    </p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const client = ref(null);
const route = useRoute();

onMounted(async () => {
  const id = route.params.id;
  try {
    console.log("Fetching client data for ID:", id); // Log pour vérifier l'ID
    const response = await axios.get(`http://127.0.0.1:5000/api/client/${id}`);
    console.log("Client data received:", response.data); // Log pour vérifier les données reçues
    if (response.data && response.data.length > 0) {
      client.value = response.data[0]; // Extraction du premier élément du tableau
    } else {
      console.error("Aucune donnée client trouvée.");
    }
  } catch (error) {
    console.error("Erreur lors du chargement des infos client :", error);
  }
});
</script>

<style scoped>
.client-card {
  background: #f9f9f9;
  padding: 1rem 2rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
