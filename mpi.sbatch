#!/bin/bash

#SBATCH --job-name=cl_final_project
#SBATCH --ntasks=10
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr

module load mpi4py/3.0.1a0_py3

mpirun -n 10 python ./get_following_mpi.py
