#!/bin/bash

# Vérifie si le script Python existe
if ! [ -f "extract_mesure.py" ]; then
    echo "Error: extract_mesure.py not found in the current directory."
    exit 1
fi

# Créer un dossier pour les fichiers .dat s'il n'existe pas déjà
output_directory="energies_files"
mkdir -p "$output_directory"

# Parcourir tous les fichiers qui correspondent au motif rs_**.out
for file in rs_*.out; do
    # Vérifie si le fichier existe pour éviter les erreurs si aucun fichier ne correspond
    if [ -f "$file" ]; then
        # Retirer l'extension .out pour générer le nom du fichier de sortie
        base_name="${file%.out}"
        output_file="${output_directory}/${base_name}.dat"  # Fichier .dat dans le dossier dat_files

        # Lancer le script Python avec les fichiers d'entrée et de sortie
        echo "Processing $file -> $output_file"
        python3 extract_mesure.py "$file" "$output_file" Etot
    else
        echo "No files found matching pattern rs_*.out"
        exit 1
    fi
done

