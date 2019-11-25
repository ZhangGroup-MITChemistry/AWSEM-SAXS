import sys
import os
import math
import numpy

sim=sys.argv[1]

main_dir = '/nobackup1/binz/aplatham/vec_test/4djg_table/'
start1=['_run/','_run_1/','_run_2/','_run_3/','_run_4/','_run_5/']
error=[]
for i in range(0,6):
    folder1 = sim + start1[i]
    os.chdir(main_dir + folder1)
    os.system('pwd')
    for j in range(0, 4):
        run = str(int(j) + 1)
        folder2 = 'run' + run + '/'
        os.chdir(main_dir+folder1+folder2)
        os.system('python select_colvars_traj.py 25')
        colvars_file='out_temp'+str(j+1)+'.colvars.traj'
        os.system('cp out_fixed300.colvars.traj ../'+colvars_file)
    os.chdir(main_dir + folder1)
    os.system('python combine_colvars.py out_temp1.colvars.traj out_temp2.colvars.traj out_temp3.colvars.traj out_temp4.colvars.traj')
    os.system('python calc_error.py combined_colvars.traj 4djg.pr')
    error_file='error.dat'
    f=open(error_file,'r')
    line=f.readline()
    line_split=line.split()
    error.append(line_split[1])
os.chdir(main_dir)
new_file='error_analysis'+sim+'.dat'
new=open(new_file,'w')
force_const = ['0.005', '0.002', '0.01', '0.001', '0.0005', '0.0001']
for i in range(0,6):
    new.write(force_const[i]+' '+error[i]+'\n')
new.close()
