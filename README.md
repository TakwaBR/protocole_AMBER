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
**Pour effectuer un recuit simulé de la molécule seule dans le vide, ces étapes suffisent:**
```bash
tleap
> source leaprc.protein.ff19SB
> mol = sequence { ACE VAL PRO PRO PRO VAL PRO PRO ARG ARG ARG NHE }
> saveamberparm mol mol.parm mol.rst7
```

## Génération des fichiers de contraintes

Pour générer les fichiers de contraintes, plusieurs outils sont disponibles. Cependant, ces outils requièrent un format spécifique de fichier, il est donc nécessaire de formater correctement vos fichiers d'entrée.

### Contraintes de distances (NOE) : utilisez la commande `makeDIST_RST`
Format du fichier d'entrée :
Le fichier doit être structuré avec les colonnes suivantes :

- `Res1_id` : ID du premier résidu
- `Res1_nom` : Nom du premier résidu
- `Atome1_nom` : Nom de l'atome dans le premier résidu
- `Res2_id` : ID du second résidu
- `Res2_nom` : Nom du second résidu
- `Atome2_nom` : Nom de l'atome dans le second résidu
- `Distance_inf` : Limite inférieure de la distance
- `Distance_sup` : Limite supérieure de la distance

Vous pouvez trouver un exemple de fichier structuré sous ce lien : [data/contraintes_noe.dist](https://github.com/TakwaBR/protocole_AMBER/blob/main/data/contraintes_noe.dist)

```text
2  VAL  HB  3  PRO  HD3  1.8  3
3  PRO  HD2  2  VAL  HA  1.8  2.3
```

Vous pouvez exécuter cette commande depuis la machine iseran :
```bash
/usr/local/amber22/bin/makeDIST_RST -ual contraintes_noe.dist -pdb mol.pdb -rst contraintes_noe.rst -map /usr/local/amber22/dat/map.DG-AMBER
```
Arguments :
- `-ual` : fichier d'entrée bien formaté
- `-pdb` : fichier PDB de votre molécule
- `-rst` : fichier de sortie
- `-map` : fichier nécessaire au fonctionnement de `makeDIST_RST`

Génération du fichier PDB :
Vous pouvez générer le fichier PDB à partir des fichiers de topologie et de coordonnées en utilisant cette commande:
```bash
$AMBERHOME/bin/ambpdb -p mol.parm7 -c mol.rst7 > mol.pdb
```
Vous pouvez trouver un exemple de fichier de sortie sous ce lien : [results/contraintes_noe.rst](https://github.com/TakwaBR/protocole_AMBER/blob/main/results/contraintes_noe.rst)

### Contraintes d’angles (<sup>3</sup>J-coupling) : utilisez la commande `makeANG_RST`
Format du fichier d’entrée :
Le fichier doit être structuré avec les colonnes suivantes :

- `Res_id` : ID du résidu
- `Res_nom` : Nom du résidu
- `J-couple` : Atomes couplés (indiquez les atomes concernés par le couplage J)
- `ConstanteJ_inf` : Limite inférieure de la constante J
- `ConstanteJ_sup` : Limite supérieure de la constante J

Vous pouvez trouver un exemple de fichier structuré sous ce lien : [data/contraintes_jcoupling.dist](https://github.com/TakwaBR/protocole_AMBER/blob/main/data/contraintes_jcoupling.dist)

```text
6  VAL  JHNA  6.5  8.5
9  ARG  JHNA  5.1  7.1
```
```bash
/usr/local/amber22/bin/makeANG_RST -pdb mol.pdb -con contraintes_jcoupling.dist -lib /usr/local/amber22/dat/tordef.lib > contraintes_jcoupling.rst
```

Arguments :
- `-pdb` : fichier PDB de votre molécule
- `-con` : fichier d’entrée bien formaté contenant les informations sur les atomes couplés
- `-lib` : fichier de la librairie de `makeANG_RST`. Vous pouvez le copier dans votre répertoire et le modifier si nécessaire.
- `contraintes_jcoupling.rst` : fichier de sortie contenant les contraintes générées

Vous pouvez trouver un exemple de fichier de sortie sous ce lien : [results/contraintes_jcoupling.rst](https://github.com/TakwaBR/protocole_AMBER/blob/main/results/contraintes_jcoupling.rst)

### Contraintes d’angles Phi/Psi/Chi 1 : utilisez la commande `makeANG_RST` et le logiciel `TALOS-N`

Vous pouvez trouver un exemple de fichier structuré pour `TALOS-N` sous ce lien: [data/talosn_input.txt](https://github.com/TakwaBR/protocole_AMBER/blob/main/data/talosn_input.txt)

Après l'exécution de `TALOS-N`, il est nécessaire de reformater le fichier de sortie afin de le préparer pour l'entrée dans `makeANG_RST`. Vous pouvez utiliser le script [src/talosn_reformat.py](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/talosn_reformat.py) pour effectuer cette conversion.

```bash
python3 talosn_reformat.py pred.tab contraintes_phipsi.dist
```
Vous pouvez trouver un exemple de fichier de sortie sous ce lien: [data/contraintes_phipsi.dist](https://github.com/TakwaBR/protocole_AMBER/blob/main/data/contraintes_phipsi.dist)

Il est essentiel de supprimer les angles pour lesquels `TALOS-N` n'a pas effectué de prédiction (c'est-à-dire ceux ayant une valeur de 9999.000). Si vous disposez des informations sur les angles CHI, vous pouvez également les ajouter.

Vous pouvez désormais générer le fichier de contraintes en utilisant `makeANG_RST`
```bash
/usr/local/amber22/bin/makeANG_RST -pdb mol.pdb -con contraintes_phipsi.dist -lib tordef.lib > contraintes_angles.rst
```
Arguments :

- `-pdb` : fichier PDB de votre molécule
- `-con` : fichier d'entrée correctement formaté
- `-lib` : fichier de la librairie de makeANG_RST. Vous pouvez le copier dans votre répertoire et le modifier si nécessaire.
- contraintes_angles.rst est le fichier de sortie

### Contraintes de chiralité et de conformation cis/trans: utilisez la commande `makeCHIR_RST`
Le fichier de contraintes de chiralité et de conformation peut être généré à partir du fichier PDB de la molécule seulement.

```bash
/usr/local/amber22/bin/makeCHIR_RST mol.pdb angles_impropres.rst
```
### Génération du fichier contenant l'ensemble des contraintes RMN
Une fois tous les fichiers de contraintes générés, il est nécessaire de les concaténer en un seul fichier.
```bash
cat contraintes_noe.rst contraintes_jcoupling.rst contraintes_angles.rst angles_impropres.rst > contraintes_rmn.rst
```
Vous pouvez trouver un exemple de fichier de sortie sous ce lien: [results/contraintes_rmn.rst](https://github.com/TakwaBR/protocole_AMBER/blob/main/results/contraintes_rmn.rst)

## Recuit simulé
**Assurez-vous de vous placer dans le dossier iseran:/data/votre-nom avant de lancer les simulations !**

### Minimisation de la structure
Avant de lancer le recuit simulé, il est nécessaire d'effectuer une minimisation de la structure.

Un exemple de fichier de minimisation est disponible via le lien suivant: [src/minimisation_vide.in](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/minimisation_vide.in)

```bash
/usr/local/amber22/bin/pmemd.cuda -O -i minimisation_vide.in -o minimisation_vide.out -p mol.parm7 -c mol.rst7 -r minimisation_vide.ncrst -x minimisation_vide.nc -inf minimisation_vide.info &
```

Arguments :

- `-O` : écrase les fichiers de sortie déjà existants
- `-i` : fichier d'entrée pour la minimisation
- `-o` : fichier de sortie contenant les informations sur les énergies pendant la minimisation
- `-p` : fichier de topologie
- `-c` : fichier de coordonnées
- `-r` : fichier de sortie pour les coordonnées "restart"
- `-x` : fichier de sortie pour les trajectoires
- `-inf` : fichier d'informations supplémentaires

### Création de dossiers pour les fichiers de sortie
Il est recommandé de créer des dossiers dédiés pour organiser les fichiers de sortie du recuit simulé.
```bash
mkdir OUT
mkdir NC
mkdir NCRST
mkdir INFO
```
### Lancement du recuit simulé
Un exemple de fichier de recuit simulé est disponible via le lien suivant: [src/recuit_simule.in](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/recuit_simule.in)

Un script bash permettant de lancer 100 simulations par lots de 2 est disponible via le lien suivant: [src/recuit_simule.sh](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/recuit_simule.sh)

```bash
chmod +x recuit_simule.sh
```
Cette commande rend le script `recuit_simule.sh` exécutable, permettant son lancement direct en tant que programme.

Vous pouvez à présent lancer le recuit simulé
```bash
./recuit_simule.sh
```
### Choix des meilleures structures
Pour sélectionner les meilleures structures RMN produites, vous pouvez utiliser le script bash [src/extract_all_energy.sh](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_all_energy.sh) qui utilise le script Python [src/extract_mesure.py](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_mesure.py) pour extraire toutes les énergies totales des simulations et créer des fichiers `.dat` dans un nouveau dossier nommé `energies_files`.

```bash
chmod +x extract_all_energy.sh
./extract_all_energy.sh
```
Utilisez le script bash [src/extract_last_energy.sh](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_last_energy.sh)  pour extraire les énergies finales de chaque simulation et les trier par ordre croissant. Le classement sera écrit dans un fichier de sortie nommé `energies_last_values_sorted.txt`

```bash
chmod +x extract_last_energy.sh
./extract_last_energy.sh
```
