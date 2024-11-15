"""
This script processes a prediction data file with φ and ψ angles for residues, 
converting them into constraints in the required format.

It reads the input file containing residue information, adjusts the φ and ψ values 
by their standard deviations, and writes the results to an output file.

Arguments:
    input_file (str): Path to the input file containing prediction data.
    output_file (str): Path to the output file for saving the results.

Usage:
    python3 script.py input_data.txt output_data.txt
"""

import argparse

# Dictionary of residues
aa = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS",
    "E": "GLU", "Q": "GLN", "G": "GLY", "H": "HIS", "I": "ILE",
    "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO",
    "S": "SER", "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL"
}


# Main function to process the files
def process_files(input_file, output_file):
    """
    Processes the input file, extracts φ/ψ angle data, and writes the constraints 
    in the specified output file.

    Args:
        input_file (str): Path to the input file containing the prediction data.
        output_file (str): Path to the output file where results will be written.
    """
    # Open the input and output files
    with open(input_file, 'r') as filin, open(output_file, "w") as filout:
        found_format = False  # Flag to mark when "FORMAT" is found

        for ligne in filin:
            # If the line starts with "FORMAT", begin processing subsequent data
            if ligne.startswith("FORMAT"):
                found_format = True
                continue # Skip to the next line after finding "FORMAT"

            # Once "FORMAT" is found, process the subsequent lines
            if found_format:
                if ligne.strip() == "":  # Skip empty lines
                    continue
                # Extract necessary data from the line
                resnum, resname, phi, psi, sdphi, sdpsi = ligne[:43].split()
                # Replace the residue code with the full residue name
                if resname in aa:
                    resname = aa[resname]

                # Write the results to the output file in the required format
                filout.write(f"{int(resnum)+1:4d} {resname:<3} PHI {float(phi)-float(sdphi):8.3f} {float(phi)+float(sdphi):8.3f}\n")
                filout.write(f"{int(resnum)+1:4d} {resname:<3} PSI {float(psi)-float(sdpsi):8.3f} {float(psi)+float(sdpsi):8.3f}\n")

# Main script to handle argument parsing
if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process a prediction data file and generate phi/psi constraints.")

    # Add input and output file arguments
    parser.add_argument("input_file", type=str, help="The input file containing the data.")
    parser.add_argument("output_file", type=str, help="The output file to save the results.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to process the specified files
    process_files(args.input_file, args.output_file)
