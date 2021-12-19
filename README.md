# Projet euro Million

Le but de ce projet est de créer une API qui fait des prédictions sur le tirage de l'Euro Million.


## Choix technique

Nous indiquerons comment installer les librairies dans la partie *Installation*.

Nous avons décidé d'utiliser *Fast API* afin de créer notre API, ce qui nous permet de créer notre API facilement.

Pour le modèle prédictif nous avons choisi d'utiliser un algorithme *random forest*, venant de la libraire *sklearn*. Nous avons choisi cet algotithme car nous devions faire du machine learning.
Nous avons aussi utilisé la librairie *pandas* pour la gestion de data frame.

## Instalation

Pour installer *Fast API* nous avons utlisé la ligne de commande : "pip install "fastapi[all]".

Pour installer les librairies python *sklearn* et *pandas* nous avons utilise les commandes : "pip install sklearn" et "pip install pandas".

## Utilisation

Pour utiliser l'API (après avoir installé les librairies données précedemment): 
<br/>   - ouvrir un terminal dans le dossier racine du projet et lancer la commande "uvicorn api.main:app -- reload"
<br/>   - se rendre sur page web http://127.0.0.1:8000/docs#/
<br/>   - lancer la requête "retrain" afin d'entraîner le modèle

Pour la requête PUT /api/model/ : la date doit être un string, les autres valeurs des entiers

Pour la requête POST /api/predict/ : 
<br/>   - les valeurs doivent être entre 1 et 50 pour les nombres classiques (sans doublon)
<br/>   - les valeurs doivent être entre 1 et 12 pour les nombres étoiles (sans doublon)
