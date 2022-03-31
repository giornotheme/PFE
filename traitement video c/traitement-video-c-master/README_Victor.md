# Développement de la partie vidéo du projet PERSEUS sur le lanceur ASTREOS

## Initialisation de la Raspberry pi 4 :

image : preemptPi (2 557 293 ko)

Flasher preemptPi avec BalenaEtcher sur une carte SD
La carte SD devrait s'appeler "boot" sur votre pc maintenant
Rentrez dans la carte SD et créez un fichier "ssh" sans extension

Avec MobaXterm ajoutez une nouvelle session : 
- en haut à gauche cliquez sur session
- cliquez sur SSH
- dans Remote Host écrivez "raspberrypi.local"
- cochez Specify username et écrivez "pi"
- cliquez sur ok

A gauche double cliquez sur raspberrypi.local, vous devriez être dans la raspi maintenant.
ensuite écrivez "hostname -I", une adresse IP devrait s'afficher

Refaites la manipulation pour ajoutez une nouvelle session mais au lieu de mettre "raspberrypi.local" mettez l'adresse IP qui était affichée
du coup maintenant à gauche vous avez 2 sessions : la première avec "raspberrypi.local" et la deuxieme qu'on vient de créer avec l'adresse IP
Vous pouvez supprimer la session avec "raspberrypi.local", on va travailler que avec l'adresse IP.

Double cliquez sur la session avec l'adresse IP
Vous êtes maintenant dans la raspberry

Faut maintenant configurer internet :
- sudo raspi-config
- network options
- Si c'est une premiere connexion faut choisir un pays : Selectionnez France
- Wireless LAN
- Entrez le SSID de votre réseau
- Entrez le mot de passe de votre réseau
Normalement vous avez internet : pour tester écrivez : ping 8.8.8.8

## Pour OpenCV sur Python : 
```
- sudo apt update
- sudo apt-get install -y libopencv-dev python-opencv python-picamera libwebp-dev libtiff5 libilmbase-dev libopenexr-dev libgstreamer1.0-dev
```
Normalement vous avez opencv et python d'installés maintenant

Branchez la caméra à la raspi (regardez des vidéos yt)

A gauche sur l'arbre des dossiers, uploadez les fichiers "receiver.py", "sender.py" et "enable_i2c_vc.sh" 
Faut lancer le script sh maintenant : 
```
- chmod +x enable_i2c_vc.sh
- sh enable_i2c_vc.sh
```

Maintenant on peut prendre une photo :
```
- raspistill -o image.jpg 
```
A gauche, revenez au dossier home/pi et normalement vous avez "image.jpg" qui s'est ajouté. Double-cliquez dessus et l'image devrait apparaitre

## Pour OpenCV en C:

Uploader OpenCV-4-5-2.sh dans votre raspi et executez le :
```
- sh OpenCV-4-5-2.sh
```
Après cela il faut installer des librairies :
``` 
- sudo apt-get install libasio-dev (version non boost, c'est notre cas)
```
Ensuite on se place dans traitement-video-c/udpAsio/cudp et :
```
- mkdir build
- cd build
- cmake ../
- make clean
- make
```
S'il n'y a pas d'erreur c'est que le programme s'est compilé correctement
Il reste plus qu'à exécuter le programme :
```
- cUDPsender [L'ADRESSE IPV4 DE VOTRE ORDI]
```
### Sur Linux : 

Même manipulation, et pour exécuter le receiver : 
```
- cUDPreceiver [L'ADRESSE IPV4 DE VOTRE ORDI]
```
