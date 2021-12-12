# Commandes Pour l'Installation & le Lancement

## Environnement Virtuel

Pour créer un environnement virtuel, il faut se déplacer dans le dossier principal (AccordeurGuitare)puis lancez la commande suivant dans la ligne de commande suivant.

```bash
python -m venv venv
```

Ensuite, toujours dans le même dossier lancez la commande suivante pour activer l'environnement virtuel.

```bash
.\venv\Scripts\activate.bat
```

## Installation des Modules

Pour installer les différents modules, tout d'abord activez l'environnement virtuel. Ensuite, Avec l'environnement virtuel activé et en se trouvant dans le dossier 'AccordeurGuitare', lancez la commande suivante.

```bash
pip install -r .\requirements.txt
```

## Lancement du Programme

Enfin, pour lancer du programme depuis le dossier principale (AccordeurGuitare), éxécutez un par un les commandes suivantes.

```bash
cd .\Main\
python .\main.py
```
