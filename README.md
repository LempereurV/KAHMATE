# KAHMATE
Ce dossier contient le code et toutes les données nécessaires afin pouvoir jouer au jeu de société Kahmaté. Le dossier contient toutes les données ayant servi lors d'un projet pour le cours de Techniques de Développement Logiciel (TDLOG). Il a été réalisé par Vianney DE MONICAULT, Erwann ESTEVE, Félix FOURREAU et François GOURGUE.

## Bibliothèques à installer
Pour pouvoir lancer le jeu correctement, il est nécessaire d'installer plusieurs bibliothèques Python:
- **tensorflow**: attention, tensorflow n'est à priori pas téléchargeable avec Python 3.12
- **keras**: utilisé avec tensorflow pour le bot de Deep Reinforcement Learning
- **pygame**: attention, l'interface graphique ne s'ouvre pas à priori avec une distribution Linux

## Lancement de la partie
Afin de lancer la partie, il suffit d'exécuter le fichier *main.py*. La hiérarchie des fichiers risque de provoquer des erreurs d'exécution si on exécute directement un fichier qui n'est pas dans le dossier principal.

Si un joueur souhaite passer son tour, il doit cliquer sur l'icone "KAHMATE" la plus proche de sa ligne d'essai (Le logo kahamate du bas pour les rouges du haut pour les bleus). 

## Fonctionnement du bot fonctionnant avec du Deep Reinforcement Learning
Le bot ne peut commencer à choisir son prochain coup que lorsque son adversaire a fini de jouer. Si le bot ne semble pas jouer ses deux coups au bout d'une dizaine de secondes, il est possible qu'il ait choisi de jouer un seul coup. Pour le remarquer, il faut regarder dans le terminal si le bot est encore en train de calculer son meilleur coup possible.    

