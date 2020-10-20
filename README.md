__Création d'un environnement virtuel__
=======================================
1. Sur Ubuntu, **sudo apt-get instal virtualenv** pour installer l'environnement virtuel python
2. Pour activer le venv, **source venv/bin/activate**
3. Pour installer flask dans le venv, **pip3 install flask**
4. Pour quitter le venv, **deactivate**

__Installer les librairies__
============================
1. Activer l'environnement virtuel : **source venv/bin/activate**
2. Installer les deux librairies :
    * **pip install flask-WTF**
    * **pip install flask-login**
3. Quitter le venv : **deactivate**

__Première méthode__ (manuellement)
====================
1. Lancer l'environnement virtuel : **source venv/bin/activate**
2. Se placer dans le bon fichier (TP01 ici) : **cd Desktop/flask/TP02**
3. Autoriser ou non le mode DEBUG : **export FLASK_DEBUG=1**
4. Exporter le fichier flask_engine.py : **export FLASK_APP=flask_engine.py**
5. Exécuter ce fichier : **flask run**

__Seconde méthode__ (avec le Makefile)
===================
1. Lancer l'environnement virtuel : **source venv/bin/activate**
2. Se placer dans le bon fichier (TP01 ici) : **cd Desktop/flask/TP02**
3. Exécuter le code : **make run**
4. Eventuellemnt supprimer le dossier __ pycache __ qui a été créé : **make clear**


__Se connecter en tant qu'admin sur le système__
================================================
1. Lancer la To Do App : **Voir les 2 différentes méthodes ci-dessus.**
2. Rentrer **admin** dans **username**
3. Utiliser **2020%dmr** comme **mot de passe**.
4. Envoyer le formulaire avec le bouton **Send**.
