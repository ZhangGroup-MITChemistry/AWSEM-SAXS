import sys
import os
import math
import numpy

# Combines collective variables trajectories from annealing to a single temperature trajectory
# Useage: python select_colvars_traj.py
# parameters: delay=colvars traj steps to skip for equilibration; Temp_list= annealing temperatures; select=temp # to create a cmpared file
# Check names of files: out_temp$Temp.colvars.traj and log.lammps are defaults

delay=5000
Temp_list=['300','340','380','420','460','500']
select='0'

# Get the index from log file
log_file='log.lammps'
log=open(log_file,'r')
line=log.readline()
line=log.readline()
line=log.readline()
line=log.readline()
index_list=[]
while line:
    if len(line)>0:
        line_split=line.split()
        for i in range(1,len(line_split)):
            if line_split[i]==select:
                index_list.append(i-1)
    line=log.readline()

colvars_data=[]
for i in range(0,len(Temp_list)):
    colvars_file='out_temp'+Temp_list[i]+'.colvars.traj'
    colvars_temp=numpy.loadtxt(colvars_file)
    colvars_data.append(colvars_temp)

colvars_data_300=numpy.zeros((len(index_list)-delay,len(colvars_data[0][0])))
for i in range(0,len(index_list)):
    if i>(delay-1):
        colvars_data_300[i-delay]=colvars_data[index_list[i]][i]

numpy.savetxt('out_fixed300.colvars.traj',colvars_data_300)
