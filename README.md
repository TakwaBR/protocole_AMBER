# Protocole: Calcul de structure RMN suivi de simulations de dynamique moléculaire en utilisant AMBER23 GPU
## Construction du système
La construction du système d'intérêt peut être réalisée à l'aide des programmes **tleap** ou **xleap**. Contrairement à **tleap**, **xleap** offre une interface graphique. Dans ce protocole, la procédure de construction sera illustrée en utilisant **tleap**.
Pour utiliser tleap, l'environnement conda AmberTools23 doit d'abord être activé :
```bash
conda activate AmberTools23
```
Avant de construire le système, il est nécessaire de sélectionner le champ de force à utiliser. Dans ce cas, le champ de force choisi est ff19SB.
```bash
tleap
> source leaprc.protein.ff19SB # Import de la bibliothèque du champ de force
```
La molécule peut être construite à partir de sa séquence ou importée depuis un fichier PDB
```bash
> mol = sequence { ACE VAL PRO PRO PRO VAL PRO PRO ARG ARG ARG NHE }
```
ou
```bash
> mol = loadpdb fichier_mol.pdb
```
- Sélectionnez le modèle d’eau à utiliser. Le modèle OPC est recommandé pour une compatibilité optimale avec le champ de force ff19SB.
```bash
> source leaprc.water.opc # Import de la bibliothèque du modèle d'eau
```
- Ajoutez des molécules d'eau au système en définissant les dimensions et la forme de la boîte de simulation.
```bash
> solvateoct mol OPCBOX 10.0
```
- Les ions peuvent maintenant être ajoutés au système.
  ```bash
  > charge mol # Permet de déterminer la charge totale de la molécule
  > addIons2 mol Cl- 0 # Ajout d’ions pour neutraliser le système
  ```
  L'argument 0 indique que le programme doit ajouter automatiquement le nombre d'ions nécessaires pour neutraliser la charge du système.
- Si nécessaire, ajoutez d'autres ions au système :
  ```bash
  > addIons2 mol Na+ 8 Cl- 8
  ```
- Enregistrez ensuite les fichiers de topologie et de coordonnées du système :
```bash
> saveamberparm mol mol.parm mol.rst7
```
** Pour effectuer un recuit simulé de la molécule seule dans le vide, ces étapes suffisent: **
```bash
tleap
> source leaprc.protein.ff19SB
> mol = sequence { ACE VAL PRO PRO PRO VAL PRO PRO ARG ARG ARG NHE }
> saveamberparm mol mol.parm mol.rst7
```

