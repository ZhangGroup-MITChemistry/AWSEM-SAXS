import sys
import os
import math
import numpy

numpy.set_printoptions(threshold=numpy.nan)
# File to make the next alphas for a prbias simulation
# Inputs: alpha file from previous simulation (old_alpha_file), histogram of pr from previous
# simulation (f_sim.txt), pr data from experiment (pr_file), temperature (temp),
# tolerance for convergence (tol), factor to get rid of low frequency modes (cutEig),
# number of atoms used in the p(r) (natoms) number of previous iterations (num_iter)
# Usage:
# python iterate_alpha2.py old_alpha_file colvars_file pr_file temp tol cutEig force_const

if len(sys.argv)!=8:
    print("Incorrect usage. Please input proper files:")
    print("python iterate_alpha.py old_alpha_file colvars_file pr_file temp tol cutEig force_const")
    print("Quiting")
    exit()


# Get alpha from previous iteration
old_alpha_file=sys.argv[1]
old_alpha=numpy.loadtxt(old_alpha_file)
length=len(old_alpha)

# get pr from simulation
# Number of other collective varibles. Useful for parsing.
collective_vars=0
print('Make sure prbias is first collective variable and that 2 other collective variables are included in the file...')
colvars_file=sys.argv[2]
colvars_data=numpy.loadtxt(colvars_file)
# simulated data matrix. Each row corresponds to a particular timestep
f_sim=colvars_data[:,0:(len(colvars_data[1,:])-(collective_vars))]
# Average of each column is the average distribution from the simulation
f_sim_ave=numpy.average(f_sim,0)
print(f_sim_ave)

# get pr from experiment
pr_file=sys.argv[3]
pr_data=numpy.loadtxt(pr_file)
r=pr_data[:,0]
f_exp=pr_data[:,1]

print("Read in data...")





# Calculate error
diff=f_sim_ave-f_exp
numpy.savetxt('testing_diff.txt',diff)
# calculate the standard deviation of each element
std_dev=numpy.divide(numpy.std(f_sim,axis=0),f_sim_ave,where=f_sim_ave!=0)
# Calculate overall error
error=sum(abs(diff))/sum(f_exp)
# Check for convergence
error_file="error.dat"
tol=float(sys.argv[5])
if error < tol:
    print("Alpha has converged!!! No new alpha necessary")
    exit()
else:
    print("Not yet converged, calculating next alpha...")
err=open(error_file,'w')
err.write('Error: '+str(error)+'\n')
for i in range(0,len(std_dev)):
    err.write(str(std_dev[i])+'\n')
# leave open to write size of dalpha


# Which one should I use? For now, using B1 Note: they are essentially equivalent, numpy.cov is faster
# Calculate Covariance Matrix B
B1=numpy.cov(f_sim,None,0)

#B=numpy.zeros((length,length))
#for k in range(0,len(f_sim)):
#    for i in range(0,length):
#        for j in range(i,length):
#            B[i,j]=B[i,j]+f_sim[k][i]*f_sim[k][j]
#B=B/len(f_sim)
#for i in range(0,length):
#    for j in range(i,length):
#        B[i,j]=B[i,j]-f_sim_ave[i]*f_sim_ave[j]
#        B[j,i]=B[i,j]
#numpy.savetxt('testing_B.txt',B)



print('Calculated Covariance matrix, taking inverse...')
# Check this part of the code!
# Remove some eigenvalues
cutEig=int(sys.argv[6])
U,D1,V=numpy.linalg.svd(B1)
for i in range(0,cutEig):
    print('cutting...')
    j=(len(D1)-1)-i
    D1[j]=0.0
D=numpy.zeros((length,length))
numpy.fill_diagonal(D,D1)
# AT is new matrix with removed eigenvalues, invert AT
AT=numpy.dot(numpy.dot(U,D),V)


# Calculate dalpha
kb=0.0019872041 # Boltzman Constant in kcal / mol K
temp=float(sys.argv[4])
Beta=1/(kb*temp)
force_const=float(sys.argv[7])
dalpha= (1/Beta)*numpy.dot(numpy.linalg.pinv(AT),numpy.transpose(diff))
# Add to error file
err.write('size of dalpha: '+str(numpy.linalg.norm(dalpha))+'\n')
err.close()
dalpha= ( (force_const * dalpha)/numpy.linalg.norm(dalpha) )
numpy.savetxt('dalpha.txt',dalpha)

# Update alpha
alpha = old_alpha + dalpha

# Save to new file
new_file='new_alpha.txt'
numpy.savetxt(new_file,alpha)

print('Done')
