# Protocole: Calcul de structure RMN suivi de simulations de dynamique moléculaire en utilisant AMBER23 GPU

Ce protocole décrit les étapes nécessaires à la préparation et à la simulation d'une molécule biologique à l'aide du logiciel AMBER23 et de son support GPU. L'objectif principal est d'étudier la dynamique moléculaire d'une molécule à partir de la construction du système, l'ajout de solvants et d'ions, jusqu'à la phase finale de production en dynamique moléculaire. Ce processus inclut également l'incorporation de données expérimentales de RMN sous forme de contraintes, telles que des distances NOE, des constantes de couplage J et des angles de torsion, pour affiner la structure et guider la simulation.

**Auteur:** Takwa Ben Radhia

## Construction du système
La construction du système d'intérêt peut être réalisée à l'aide des programmes **tleap** ou **xleap**. Contrairement à **tleap**, **xleap** offre une interface graphique. Dans ce protocole, la procédure de construction sera illustrée en utilisant **tleap**.
Pour utiliser **tleap**, l'environnement conda **AmberTools23** doit d'abord être activé :
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

Vous pouvez exécuter cette commande depuis la machine Iseran :
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

### Contraintes d’angles Phi/Psi/Chi 1 : utilisez la commande `makeANG_RST` et le logiciel **TALOS-N**

Vous pouvez trouver un exemple de fichier structuré pour **TALOS-N** sous ce lien: [data/talosn_input.txt](https://github.com/TakwaBR/protocole_AMBER/blob/main/data/talosn_input.txt)

Après l'exécution de **TALOS-N**, il est nécessaire de reformater le fichier de sortie afin de le préparer pour l'entrée dans `makeANG_RST`. Vous pouvez utiliser le script [src/talosn_reformat.py](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/talosn_reformat.py) pour effectuer cette conversion.

```bash
python3 talosn_reformat.py pred.tab contraintes_phipsi.dist
```
Vous pouvez trouver un exemple de fichier de sortie sous ce lien: [data/contraintes_phipsi.dist](https://github.com/TakwaBR/protocole_AMBER/blob/main/data/contraintes_phipsi.dist)

Il est essentiel de supprimer les angles pour lesquels **TALOS-N** n'a pas effectué de prédiction (c'est-à-dire ceux ayant une valeur de 9999.000). Si vous disposez des informations sur les angles CHI, vous pouvez également les ajouter.

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
**Assurez-vous de vous placer dans le dossier *iseran:/data/votre-nom* avant de lancer les simulations !**

Copiez les fichiers nécessaires sur la machine Iseran en utilisant la commande `scp`.

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
### Sélection et extraction des meilleures structures
Pour sélectionner les meilleures structures RMN, c'est-à-dire celles avec l'énergie finale la plus basse, vous pouvez utiliser le script bash [src/extract_all_energy.sh](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_all_energy.sh) qui utilise le script Python [src/extract_mesure.py](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_mesure.py) pour extraire toutes les énergies totales des simulations et créer des fichiers `.dat` dans un nouveau dossier nommé `energies_files`.

```bash
chmod +x extract_all_energy.sh
./extract_all_energy.sh
```
Utilisez le script bash [src/extract_last_energy.sh](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_last_energy.sh)  pour extraire les énergies finales de chaque simulation et les trier par ordre croissant. Le classement sera écrit dans un fichier de sortie nommé `energies_last_values_sorted.txt`

```bash
chmod +x extract_last_energy.sh
./extract_last_energy.sh
```

Après avoir sélectionné vos meilleures structures, récupérez leurs fichiers de trajectoire `.nc` et copiez-les sur votre machine locale en utilisant la commande `scp`. N'oubliez pas d'activer l'environnement conda **AmberTools23**. 
Avant de procéder à la simulation de dynamique moléculaire, il est nécessaire de générer les fichiers de topologie `.parm` et de coordonnées `.rst`. Une fois ces fichiers générés, vous pourrez ajouter la boîte d'eau et les ions pour préparer les structures.

Commencez par récupérer la dernière frame de la simulation au format PDB à l'aide de **cpptraj**.
```
cpptraj
> parm mol.parm7
> trajin rs_1.nc lastframe
> trajout rs_1.pdb pdb
> run
```
Nous pouvons maintenant générer les fichiers de trajectoire et de coordonnées nécessaires pour la simulation:
```bash
tleap
> source leaprc.protein.ff19SB
> molecule = loadpdb rs_1.pdb
> source leaprc.water.opc
> solvateoct molecule OPCBOX  10.0
> addIons2 molecule Cl- 0
> addIons2 molecule Na+ 8 Cl- 8
> saveamberparm molecule rs_1.parm7 rs_1.rst7
```
Répétez cette procédure pour toutes les structures sélectionnées.

Pour chaque structure, générez les fichiers de trajectoire et de coordonnées nécessaires, puis ajoutez la boîte d'eau et les ions avant de procéder à la simulation.

## Simulation de dynamique moléculaire
Copiez vos fichiers de trajectoire et de coordonnées sur la machine Iseran.

### Minimisation du système
Une minimisation du système est indispensable avant de lancer la simulation.

Un exemple de fichier de minimisation est disponible ici : [src/md_minimisation.mdin](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/md_minimisation.mdin)

```bash
/usr/local/amber22/bin/pmemd.cuda -O -i md_minimisation.mdin -o mini_rs_1.out -p rs_1.parm7 -c rs_1.rst7 -r mini_rs_1.ncrst -inf mini_rs_1.info -ref rs_1.rst7 &
```
Arguments :

- `-O` : écrase les fichiers de sortie existants.
- `-i` : fichier d'entrée pour les paramètres de minimisation.
- `-o` : fichier de sortie contenant les énergies et informations de minimisation.
- `-p` : fichier de topologie du système.
- `-c` : fichier de coordonnées initiales.
- `-r` : fichier de coordonnées finales ("restart") de la minimisation.
- `-inf` : fichier d'informations sur l'exécution de la minimisation.
- `-ref` : fichier de référence pour appliquer les contraintes.

### Equilibrage
L'équilibrage permet de stabiliser la température et la pression du système pour préparer le système à la simulation de production.

Un exemple de fichier d'équilibrage est disponible ici : [src/md_equilibrage.mdin](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/md_equilibrage.mdin)

```bash
/usr/local/amber22/bin/pmemd.cuda -O -i md_equilibrage.mdin -o equi_rs_1.out -p rs_1.parm7 -c mini_rs_1.ncrst -r equi_rs_1.ncrst -inf equi_rs_1.info -ref rs_1.rst7 &
```

Arguments :

- `-O` : écrase les fichiers de sortie existants.
- `-i` : fichier d'entrée pour les paramètres d'équilibrage.
- `-o` : fichier de sortie contenant les énergies et informations de l'équilibrage.
- `-p` : fichier de topologie du système.
- `-c` : fichier de coordonnées issues de la minimisation.
- `-r` : fichier de coordonnées finales ("restart") de l'équilibrage.
- `-inf` : fichier d'informations sur l'exécution de l'équilibrage.
- `-ref` : fichier de référence pour appliquer les contraintes.

### Production
Nous pouvons désormais lancer la phase de production, qui consiste à simuler la dynamique moléculaire de la structure optimisée. Cette étape permettra d'observer le comportement de la molécule au cours du temps et d'analyser les propriétés thermodynamiques, telles que la température, l'énergie et la densité.

Un exemple de fichier de production est disponible ici : [src/md_production.mdin](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/md_production.mdin)

```bash
/usr/local/amber22/bin/pmemd.cuda -O -i md_production.mdin -o prod_rs_1.out -p rs_1.parm7 -c equi_rs_1.ncrst -r prod_rs_1.ncrst -inf prod_rs_1.info &
```
Arguments :

- `-O` : écrase les fichiers de sortie existants.
- `-i` : fichier d'entrée pour les paramètres de la production.
- `-o` : fichier de sortie contenant les énergies et informations de la production.
- `-p` : fichier de topologie du système.
- `-c` : fichier de coordonnées issues de l'équilibrage.
- `-r` : fichier de coordonnées finales ("restart") de la production.
- `-inf` : fichier d'informations sur l'exécution de la production.

### Analyse de la stabilité de la simulation
Vous pouvez utiliser le script Python [extract_mesure.py](https://github.com/TakwaBR/protocole_AMBER/blob/main/src/extract_mesure.py) pour extraire les énergies cinétiques, potentielles, l'énergie totale et les mesures de densité et de température tout au long de la simulation.

```bash
python3 extract_mesure.py prod_rs_1.out etot_prod_rs_1.dat Etot
```
Arguments :

- `input_file` : chemin vers le fichier d'entrée `.out` contenant les résultats de la simulation (exemple : `prod_rs_1.out`).
- `output_file` : chemin vers le fichier de sortie où les données extraites seront sauvegardées (exemple : `etot_prod_rs_1.dat`).
- `measure_type` : type de mesure à extraire du fichier d'entrée. Les options valides sont :
  - `TEMP` : température
  - `Etot` : énergie totale
  - `EKtot` : énergie cinétique totale
  - `EPtot` : énergie potentielle totale
  - `Density` : densité

Vous pouvez ensuite visualiser l'évolution de ces mesures à l'aide de l'outil **xmgrace**:
```bash
xmgrace etot_prod_rs_1.dat
```

Si vous souhaitez visualiser l'évolution de toutes les énergies simultanément, vous pouvez utiliser la commande suivante :
```bash
xmgrace etot_prod_rs_1.dat eptot_prod_rs_1.dat ektot_prod_rs_1.dat
```
