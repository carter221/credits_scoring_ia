<template>
  <div class="login-page">
    <!-- En-tête avec le nom de l'entreprise et le message de bienvenue -->
    <header class="login-header">
      <h1>Home Crédit</h1>
      <h2>Bienvenue sur l'espace Score de Crédit</h2>
    </header>

    <!-- Contenu existant de la page de connexion -->
    <main class="login-content">
      <div class="login-container">
        <h1>Connexion client</h1>
        <form @submit.prevent="goToDashboard">
          <label for="clientId">ID Client :</label>
          <input type="number" v-model="clientId" required />
          <button type="submit">Voir mon score</button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const clientId = ref('');
const router = useRouter();

const goToDashboard = () => {
  if (clientId.value) {
    router.push(`/dashboard/${clientId.value}`);
  }
};
</script>

<style scoped>
/* Couleurs principales */
:root {
  --primary-color: #ff0000; /* Rouge */
  --secondary-color: #ffffff; /* Blanc */
  --text-color: #ffffff; /* Blanc pour le texte */
}

.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: var(--primary-color); /* Fond rouge */
  color: var(--text-color); /* Texte blanc */
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--secondary-color); /* Blanc */
  margin: 0;
}

.login-header h2 {
  font-size: 1.5rem;
  color: var(--secondary-color); /* Blanc */
  margin: 10px 0 0;
}

.login-content {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  background-color: var(--secondary-color); /* Fond blanc pour contraste */
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input {
  width: 100%;
  padding: 0.5rem;
  margin: 1rem 0;
}

button {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
