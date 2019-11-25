import sys
import os
import math
import numpy

numpy.set_printoptions(threshold=numpy.nan)
# File to make check the error for alpha simulation

if len(sys.argv)!=3:
    print("Incorrect usage. Please input proper files:")
    print("python iterate_alpha.py colvars_file pr_file")
    print("Quiting")
    exit()

# get pr from simulation
# Number of other collective varibles. Useful for parsing.
collective_vars=0
print('Make sure prbias is first collective variable and that 2 other collective variables are included in the file...')
colvars_file=sys.argv[1]
colvars_data=numpy.loadtxt(colvars_file)
# simulated data matrix. Each row corresponds to a particular timestep
f_sim=colvars_data[:,0:(len(colvars_data[1,:])-(collective_vars))]
# Average of each column is the average distribution from the simulation
f_sim_ave=numpy.average(f_sim,0)
print(f_sim_ave)

# get pr from experiment
pr_file=sys.argv[2]
pr_data=numpy.loadtxt(pr_file)
r=pr_data[:,0]
f_exp=pr_data[:,1]

print("Read in data...")





# Calculate error
diff=f_sim_ave-f_exp
# calculate the standard deviation of each element
std_dev=numpy.divide(numpy.std(f_sim,axis=0),f_sim_ave,where=f_sim_ave!=0)
# Calculate overall error
error=sum(abs(diff))/sum(f_exp)
# Check for convergence
error_file="error.dat"
err=open(error_file,'w')
err.write('Error: '+str(error)+'\n')
for i in range(0,len(std_dev)):
    err.write(str(std_dev[i])+'\n')
err.close()
