# TODO

## Description
Implémentation d'une interface web permettant de modérer les messages avant de les poster sur le canal ou le groupe cible, vous pouvez suivre les étapes ci-dessous. Cette solution implique de créer une application web en PHP avec une interface HTML/CSS et JavaScript pour gérer les interactions.

### Étape 1 : Configuration de l'Environnement
1. Serveur Web : Utilisez un serveur web comme Apache ou Nginx avec PHP installé.
2. Base de Données : Utilisez une base de données (par exemple, MySQL) pour stocker les messages en attente de modération.
3. Authentification : Mettez en place un système d'authentification pour sécuriser l'accès à la page de modération.

### Étape 2 : Modifications du Script Python
1. Envoi des Messages à la Base de Données : Modifiez votre script Python pour qu'il envoie les messages, images et vidéos récupérés depuis les canaux sources vers une base de données au lieu de les poster directement sur le canal cible.
2. Ajout d'un Statut de Modération : Chaque message doit avoir un statut de modération (en attente, accepté, refusé).

### Étape 3 : Création de l'Interface Web de Modération

Structure des Fichiers :
- index.php : Page principale pour la modération.
- style.css : Fichier CSS pour le style.
- scripts.js : Fichier JavaScript pour les interactions.
- login.php : Page de connexion.
- config.php : Fichier de configuration pour la connexion à la base de données.
- process.php : Script pour traiter les actions (accepter/refuser).

## Détails supplémentaires pour la publication sur Telegram :

1. Implémentation de l'envoi des messages acceptés sur Telegram : Ajoutez une fonction dans process.php qui utilise l'API de Telegram pour envoyer les messages acceptés au canal ou groupe cible.
2. Intégration avec le script Python : Modifiez le script Python pour écouter les messages acceptés depuis la base de données et les envoyer au canal cible.

## Protection par un compte et un mot de passe

1. Création d'un utilisateur dans la base de données
2. Vérification de l'utilisateur lors de la connexion : Utilisez des fonctions de hachage comme password_hash et password_verify pour sécuriser les mots de passe.