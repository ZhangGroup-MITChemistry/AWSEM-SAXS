import sys
import os
import math
import numpy

sim=sys.argv[1]
choose=int(sys.argv[2])

main_dir = '/nobackup1/binz/aplatham/vec_test/4djg_table/'
start1=['_run/','_run_1/','_run_2/','_run_3/','_run_4/','_run_5/']
for i in range(0,6):
    start2=start1[choose]
    folder1 = sim + start1[i]
    os.mkdir(main_dir + folder1)
    os.chdir(main_dir + folder1)
    os.system('pwd')
    old_folder = str(int(sim) - 1) + start2
    os.system('cp -r ../' + old_folder + '/* .')
    for j in range(0, 4):
        run = str(int(j) + 1)
        folder2 = 'run' + run + '/'
        os.chdir(main_dir+folder1+folder2)
        os.system('python select_colvars_traj.py 25')
        colvars_file='out_temp'+str(j+1)+'.colvars.traj'
        os.system('cp out_fixed300.colvars.traj ../'+colvars_file)
    os.chdir(main_dir + folder1)
    os.system('cp run1/alpha.txt .')
    os.system('python combine_colvars.py out_temp1.colvars.traj out_temp2.colvars.traj out_temp3.colvars.traj out_temp4.colvars.traj')
    force_const = ['0.005', '0.002', '0.01', '0.001', '0.00005', '0.0001']
    os.system('python iterate_alpha2_norm.py alpha.txt combined_colvars.traj 4djg.pr 300 0.01 18 '+force_const[i])
    for j in range(0, 4):
        folder2 = 'run' + str(int(j) + 1) + '/'
        os.chdir(main_dir + folder1 + folder2)
        os.system('cp ../new_alpha.txt alpha.txt')
        new_file='job.pbs'
        f=open(new_file,'w')
        f.write('#!/bin/bash'+'\n\n')
        f.write('#SBATCH --job-name=4djg_5\n')
        f.write('#SBATCH -N 1\n')
        f.write('#SBATCH -n 6\n')
        f.write('#SBATCH --partition=sched_mit_hill,sched_mit_binz\n')
        f.write('#SBATCH --exclude=node[250-300,460,459,008]\n')
        f.write('#SBATCH --time=12:00:00\n')
        f.write('##SBATCH --exclusive\n')
        f.write('#SBATCH --constraint=centos7\n')
        f.write('#SBATCH --mem-per-cpu=4G\n')
        f.write('##SBATCH --gres=gpu:1 \n')
        f.write('#SBATCH --export=ALL\n\n')
        f.write('module load gcc\nmodule add mvapich2/gcc\n\n')
        f.write('mpirun -np 6 /nobackup1/binz/aplatham/vec_test/Lammps-prvec2/src/lmp_openmpi -partition 6x1 -in 4djg.in')
        f.close()
        os.system('sbatch '+new_file)
