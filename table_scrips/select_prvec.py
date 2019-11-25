import sys
import os
import math
import numpy

delay=5000
Temp_list=['300','340','380','420','460','500']

len2=int(sys.argv[1])

def get_pr(filename,length):
    # get pr from simulation
    # Number of other collective varibles. Useful for parsing.
    print('Make sure prbias is first collective variable and that 2 other collective variables are included in the file...')
    f_sim2 = []
    f = open(filename, 'r')
    line = f.readline()  # first line is header
    line_split = line.split()
    pr_index = 0
    for i in range(0, len(line_split)):
        if line_split[i] == 'prbias':
            pr_index = i
    if pr_index == 0:
        print('Error: prbias flag not found in colvars_file. Make sure \'prbias\' is a header.')
        print('Exiting...')
        exit(0)
    while line:
        line_split = line.split()
        if len(line_split) > 0:
            if line_split[0] != '#':
                f_sim_timestep = []
                for i in range(0, length):
                    f_sim_timestep.append(float(line_split[pr_index + i * 2]))
                f_sim2.append(f_sim_timestep)
        line = f.readline()
    f.close()
    f_sim = numpy.asanyarray(f_sim2)
    return f_sim

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
            if line_split[i]=='0':
                index_list.append(i-1)
    line=log.readline()

colvars_data=[]
for i in range(0,len(Temp_list)):
    colvars_file='out_temp'+Temp_list[i]+'.colvars.traj'
    colvars_temp=get_pr(colvars_file,len2)
    colvars_data.append(colvars_temp)

colvars_data_300=numpy.zeros((len(index_list)-delay,len(colvars_data[0][0])))
for i in range(0,len(index_list)):
    if i>(delay-1):
        colvars_data_300[i-delay]=colvars_data[index_list[i]][i]

numpy.savetxt('out_fixed300.colvars.traj',colvars_data_300)
