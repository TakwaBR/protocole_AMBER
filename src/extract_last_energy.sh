#!/bin/bash

# Dossier contenant les fichiers
input_directory="./energies_files/"

# Fichier de sortie pour stocker les résultats triés
output_file="energies_last_values_sorted.txt"

# Vide le fichier de sortie s'il existe déjà
> "$output_file"

# Créer un fichier temporaire pour stocker les résultats non triés
temp_file=$(mktemp)

# Parcourir tous les fichiers correspondant au motif rs_*.dat
for file in "$input_directory"/rs_*.dat; do
    if [[ -f $file ]]; then
        # Extraire la dernière ligne et le deuxième champ (énergie) du fichier
        last_energy=$(tail -n 1 "$file" | awk '{print $2}')
        
        # Extraire le nom du fichier sans l'extension
        file_name=$(basename "$file" .dat)
        
        # Ajouter le nom du fichier et l'énergie dans le fichier temporaire
        echo "$file_name $last_energy" >> "$temp_file"
    fi
done

# Trier les résultats numériquement en utilisant la deuxième colonne (énergie)
# Utiliser `LC_NUMERIC` pour s'assurer que les valeurs sont bien interprétées comme des nombres flottants
LC_NUMERIC="en_US.UTF-8" sort -g -k2,2 "$temp_file" > "$output_file"

# Supprimer le fichier temporaire
rm "$temp_file"

echo "Extraction et tri complétés. Résultats sauvegardés dans $output_file."