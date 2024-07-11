# Crawler et Reposteur de Canaux Telegram

## Description

Ce script utilise la bibliothèque `telethon` pour crawler les messages de plusieurs canaux source Telegram et les reposter dans un seul canal cible. Il gère les messages texte ainsi que les médias tels que les photos et les vidéos. Le script est conçu pour s'exécuter sur un serveur sans nécessiter l'installation de l'application Telegram sur le serveur lui-même.

## Fonctionnalités

- Surveille plusieurs canaux source pour les nouveaux messages
- Reposte les messages (y compris texte, photos et vidéos) dans un canal cible
- Fonctionne en continu et traite les nouveaux messages au fur et à mesure qu'ils sont postés

## Installation

### Prérequis

- Python 3.6 ou supérieur
- Bibliothèque `telethon`

### Étapes

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/votreutilisateur/telegram-channel-crawler.git
   cd telegram-channel-crawler
   ```

2. **Configurer un environnement virtuel (optionnel mais recommandé)**

	```bash
	python -m venv venv
	source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
	```
3. **Installer les dépendances**

	```bash
	pip install -r requirements.txt
	```
## Configuration

### Créer une application Telegram

1. Allez sur [my.telegram.org](https://my.telegram.org) et connectez-vous.
2. Créez une nouvelle application et notez le `api_id` et le `api_hash`.
	

### Configurer le script

1. Modifiez config/config.json avec vos identifiants API et le canal cible :
	```
	{
    "api_id": "VOTRE_API_ID",
    "api_hash": "VOTRE_API_HASH",
    "target_channel": "canal_cible"
	}
	```
	
2. Modifiez config/channels.json pour inclure vos canaux source :
	```
	[
    "canal_source_1",
    "canal_source_2",
    "canal_source_3"
	]
	```

## Utilisation

1. Exécuter le script
	```bash
	python main.py
	```
	
2. Authentification

La première fois que vous exécutez le script, vous devrez vous authentifier en fournissant votre numéro de téléphone et le code de vérification envoyé par Telegram. Cela créera un fichier de session (session_name.session) qui stocke vos informations d'authentification.

3. Surveiller et Reposter

Le script surveillera maintenant les canaux source spécifiés et repostera automatiquement tous les nouveaux messages dans le canal cible.

## Remarques

- Assurez-vous que le compte utilisé dispose des permissions nécessaires pour lire les messages des canaux source et poster dans le canal cible.
- Le script gère les médias tels que les photos et les vidéos en plus des messages texte.
- Le script restera actif et en veille, prêt à traiter de nouveaux messages à tout moment jusqu'à ce qu'il soit arrêté.

## License

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.