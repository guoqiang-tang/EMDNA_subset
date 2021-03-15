#!/bin/bash
#SBATCH --job-name=EMDNAsubset
#SBATCH --time=0-0:10:0
#SBATCH --mem=10G
#SBATCH --account=rpp-kshook

module load python/3.7.4

source ~/ENV/bin/activate

srun python -u EMDNA_subsetting.py
