# Credit Scoring IA - Home Credit

Application web de scoring crédit pour Home Credit permettant de prédire la probabilité de remboursement d'un crédit et d'expliquer les décisions aux clients.

## Structure du Projet

- `api/` : API Flask pour servir le modèle de prédiction
- `dashboard/` : Dashboard interactif Dash pour visualiser les informations clients
- `notebooks/` : Notebooks d'exploration et de modélisation
- `models/` : Modèles entraînés et sérialisés
- `data/` : Données utilisées pour le projet

## Installation

```bash
pip install -r requirements.txt
```

## Lancement de l'application

### API

```bash
python api/app.py
```

### Dashboard

```bash
python dashboard/app.py
```

## Déploiement

L'application est déployée sur Heroku. Voir les instructions dans le fichier `deployment.md`.