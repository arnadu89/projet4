# Projet 4 de la formation OC développeur d'application python

## Guide d'installation du projet :


Dans le dossier du projet, créer l'environnement virtuel :
```
python -m venv venv
```

Activer l'environnement virtuel :
```
source venv/bin/activate
```

Installer les dépendances :
```
pip install -r requirements.txt
```

Lancer le programme :
```
python3 -m mvc_chess
```

## Guide d'utilisation du projet :
### Gérer des joueurs et des tournois :
Le programme s'utilise via le terminal.

Depuis le menu principal nous pouvons gérer les joueurs [players] et les tournois [tournaments]
```
-- MVC Chess --

1. List players
2. List tournaments
Q. Quit
Choice : 
```

La liste des joueurs permet d'ajouter et modifier les joueurs
```
-- MVC Chess --

-- Players list :
ID      Lastname    Firstname       Birthdate       Rank
0       Dupont      Jean            12/12/1992      150


1. Create a new player
2. Update a player
3. List player in alphabetical order
4. List player in rank order
M. Main menu
Q. Quit
Choice : 
```

La liste des tournois permet de créer et gérer les tournois
```
-- MVC Chess --

-- Tournaments list :
ID      Name                    Location                        Date                    Players                 State
0       Tournoi Régional 1              Paris                   04/03/2023              0/8                     Not started

1. Create a new tournament
2. View tournament detail
3. Manage a tournament
M. Main menu
Q. Quit
Choice : 
```

### Générer le rapport flake8 :
Pour générer le rapport flake8 au format html dans le dossier flake8_rapport du projet :
```
flake8
```