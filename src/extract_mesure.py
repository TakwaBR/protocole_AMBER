"""
This script is used to extract specific measurements from simulation output files (typically `.out` files).
It supports extracting temperature ("TEMP"), total energy ("Etot"), kinetic energy ("EKtot"), potential energy ("EPtot"), 
and density ("Density"). The script reads the input file, processes it based on the requested measurement type, 
and writes the extracted values to an output file in the format: `<time_step> <measurement_value>`.

Usage:
    python3 extract_mesure.py <input_file> <output_file> <measure_type>

Arguments:
    - input_file: str, path to the input `.out` file containing the simulation results.
    - output_file: str, path to the output file where the extracted data will be saved.
    - measure_type: str, type of measurement to extract from the input file. Valid options are:
        "TEMP", "Etot", "EKtot", "EPtot", "Density".

The script checks the validity of the provided measure_type and ensures that the correct number of arguments 
are passed. It handles errors gracefully, providing useful feedback when invalid arguments are provided.
"""
import sys
import re

def extraction_mesures(fichier1, fichier2, mesure):
    """
    Extract specific measurements (temperature, energy, density) from a .out file and save them in another file.

    Parameters:
    - fichier1: str, input file path containing the data (typically a .out file).
    - fichier2: str, output file path where the extracted data will be saved.
    - mesure: str, type of measurement to extract. Valid options: "TEMP", "Etot", "EKtot", "EPtot", "Density".
    
    This function reads through the input file, searches for relevant information based on the given
    measurement type, and writes the extracted values into the output file. The data is written with the
    format: <time_step> <measurement_value>.
    """
    with open(fichier1, "r") as filin, open(fichier2, "w") as filout:
        for ligne in filin:
            # Stop processing when the line starts with "A V E R A G E S"
            if ligne.startswith("      A V E R A G E S"):
                break
            # Process lines starting with "NSTEP" to extract time and corresponding measurements
            elif ligne.startswith(" NSTEP"):
                temps = ligne[30:43].strip()
                if mesure == "TEMP":
                    # Extract temperature if 'TEMP' is requested
                    temperature = ligne[53:63].strip()
                    filout.write(f"{temps} \t {temperature} \n")
            elif ligne.startswith(" Etot"):
                # Extract energy totals based on the specified measure type
                if mesure == "Etot":
                    etotale = ligne[9:25].strip()
                    filout.write(f"{temps} \t {etotale} \n")
                elif mesure == "EKtot":
                    ektotale = ligne[35:51].strip()
                    filout.write(f"{temps} \t {ektotale} \n")
                elif mesure == "EPtot":
                    eptotale = ligne[64:80].strip()
                    filout.write(f"{temps} \t {eptotale} \n")
            # Process lines containing the word "Density"
            elif re.search("( )+Density", ligne):
                if mesure == "Density":
                    densite = ligne[64:80].strip()
                    filout.write(f"{temps} \t {densite} \n")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 extract_mesure.py <input_file> <output_file> <measure_type>")
        print("Measure type options: TEMP, Etot, EKtot, EPtot, Density")
        sys.exit(1)

    # Get command line arguments
    fichier1 = sys.argv[1]
    fichier2 = sys.argv[2]
    mesure = sys.argv[3]

    # Validate that the measurement type is correct
    if mesure not in ["TEMP", "Etot", "EKtot", "EPtot", "Density"]:
        print("Error: The measurements must be one of the following: TEMP, Etot, EKtot, EPtot, Density")
        sys.exit(1)

    # Call the function to extract the requested data
    extraction_mesures(fichier1, fichier2, mesure)
