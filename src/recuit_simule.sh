#!/bin/bash
 
for i in {1..50}
do
    /usr/local/amber22/bin/pmemd.cuda -O -i recuit_simule.in -o ./OUT/rs_$((2*i-1)).out -p mol.parm7 -c minimisation_vide.ncrst -r ./NCRST/rs_$((2*i-1)).ncrst -x ./NC/rs_$((2*i-1)).nc -inf ./INFO/rs_$((2*i-1)).info &
    /usr/local/amber22/bin/pmemd.cuda -O -i recuit_simule.in -o ./OUT/rs_$((2*i)).out -p mol.parm7 -c minimisation_vide.ncrst -r ./NCRST/rs_$((2*i)).ncrst -x ./NC/rs_$((2*i)).nc -inf ./INFO/rs_$((2*i)).info &
    wait 
done
