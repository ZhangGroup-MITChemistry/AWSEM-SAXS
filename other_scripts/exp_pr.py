import sys
import os
import math
import numpy

# Calculates average p(r) from from a simulation
# Assumes the first collective variables are all the p(r). If not change the i+1 at line 34
# Useage: python exp_pr.py old_pr_file colvars_file new_file
# old_pr_file is the goal p(r), colvars_file is the collective variables output, new_file is created by this script


# Get alpha from previous simulation
old_pr_file=sys.argv[1]
old=open(old_pr_file,'r')
r=[]
line=old.readline()
while line:
    line_split=line.split()
    if len(line_split)>0:
        r.append(float(line_split[0]))
    line=old.readline()
old.close()
length=len(r)

# Get pr from simulation
colvars_file=sys.argv[2]
f_sim=[]
f=open(colvars_file,'r')
line=f.readline()
while line:
    line_split=line.split()
    if len(line_split)>0:
        if line_split[0]!='#':
            f_sim_timestep=[]
            for i in range(0,length):
                f_sim_timestep.append(float(line_split[i+1])) # Note: i + 1 because first index is time
            f_sim.append(f_sim_timestep)
    line=f.readline()
f.close()



f_exp=[]
for i in range(0,length):
    f_exp.append(0)
count=0
for i in range(0,len(f_sim)):
    for j in range(0,length):
        f_exp[j]=f_exp[j]+f_sim[i][j]
for i in range(0,len(f_exp)):
    f_exp[i]=f_exp[i]/len(f_sim)


new_file=sys.argv[3]
new=open(new_file,'w')
for i in range(0,len(f_exp)):
    new.write(str(r[i])+" "+str(f_exp[i])+'\n')
new.close()




