# Credit Scoring IA - Home Credit

Application web de scoring crédit pour Home Credit permettant de prédire la probabilité de remboursement d'un crédit et d'expliquer les décisions aux clients.

## Structure du Projet

- `api/` : API Flask pour servir le modèle de prédiction
- `dashboard/` : Dashboard interactif Dash pour visualiser les informations clients
- `notebooks/` : Notebooks d'exploration et de modélisation
- `models/` : Modèles entraînés et sérialisés
- `data/` : Données utilisées pour le projet

## Prérequis

- Python 3.8 ou supérieur
- Accès à Internet pour télécharger les dépendances
- Minimum 4 GB de RAM recommandé

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/carter221/credits_scoring_ia.git
cd credits_scoring_ia
```

### 2. Créer un environnement virtuel

```bash
# Création de l'environnement virtuel
python -m venv venv

# Activation de l'environnement
## Sur Windows
venv\Scripts\activate
## Sur macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Téléchargement des données

Les fichiers volumineux ne sont pas inclus dans le dépôt. Vous pouvez les télécharger depuis Kaggle:

Placez les fichiers CSV dans le dossier `data/`

## Lancement de l'application

### 1. Démarrer l'API backend

```bash
python api/app.py
```

L'API sera accessible à l'adresse http://localhost:5000

### 2. Démarrer le Dashboard (dans une nouvelle fenêtre de terminal)

```bash
python dashboard/app.py
```

Le dashboard sera accessible à l'adresse http://localhost:8050

## Utilisation

1. Ouvrez votre navigateur et accédez à http://localhost:8050
2. Entrez l'ID du client ou chargez un nouvel utilisateur
3. Consultez les prédictions et les explications sur la solvabilité

## Déploiement

L'application est déployée sur Heroku. Voir les instructions dans le fichier `deployment.md`.