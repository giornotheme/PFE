# Développement de la partie vidéo du projet PERSEUS sur le lanceur ASTREOS

## Instalation OpenCV 4.5.2 :
Le script OpenCV-4-5-2.sh vous permet d'installer OpenCV et ses composants.
Pour tout autre complément, vous pouvez vous réferez au lien suivant :
https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html

## Versions du programme :
Il existe deux vesrions du développement : en TCP (tcp) et en UDP (udpASIO).

### TCP :
Pour compiler :
```
$ cd ~/traitement-video-c/tcp
$ make
```

Utilisation:
```
$ ./server [port (4097 par défaut)] [port camera(0 par défaut)] &
$ ./client <Adresse serveur> <Port serveur>

```

### UDP :
Pour compiler :
```
$ cd ~/traitement-video-c/tcpudpAsio/cudp
$ mkdir build
$ cd build
$ cmake ../
$ make

```

Utilisation:
```
$ cUDPreceiver 192.168.0.1  # Ou une autre adresse
$ cUDPsender 192.169.0.1

```
