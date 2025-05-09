# Guide de Déploiement

Ce document contient les instructions pour déployer l'application Credit Scoring sur Heroku.

## Prérequis

1. Un compte [Heroku](https://www.heroku.com/)
2. [Git](https://git-scm.com/) installé sur votre machine
3. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installé sur votre machine

## Étapes de déploiement

### 1. Connexion à Heroku

```bash
heroku login
```

### 2. Création de l'application sur Heroku

```bash
heroku create homecredit-scoring
```

### 3. Configuration des variables d'environnement

```bash
heroku config:set FLASK_APP=dashboard/app.py
```

### 4. Déploiement de l'application

```bash
git push heroku main
```

### 5. Vérification du déploiement

```bash
heroku open
```

## Dépannage

Si vous rencontrez des problèmes lors du déploiement, vérifiez les logs Heroku :

```bash
heroku logs --tail
```
