# Protocole: Calcul de structure RMN suivi de simulations de dynamique moléculaire en utilisant AMBER23 GPU
## Construction du système
La construction du système d'intérêt peut être réalisée à l'aide des programmes **tleap** ou **xleap**. Contrairement à **tleap**, **xleap** offre une interface graphique. Dans ce protocole, la procédure de construction sera illustrée en utilisant **tleap**.
Pour utiliser tleap, l'environnement conda AmberTools23 doit d'abord être activé :
```bash
conda activate AmberTools23
```
- Avant de construire le système, il est nécessaire de sélectionner le champ de force à utiliser. Dans ce cas, le champ de force choisi est ff19SB.
```bash
tleap
> source leaprc.protein.ff19SB # Import de la bibliothèque du champ de force
```
