import sys
import os
import math
import numpy

# Normalizes the p(r). Can be modified to reduce the number of points to increase speed.
# Usage: old_file (unnormalized p(r)), new_file (result of this code), N (number of atoms being biased toward, our studies used alpha-Cs)

old_file=sys.argv[1]
new_file=sys.argv[2]
N=float(sys.argv[3])


data=numpy.loadtxt(old_file)

f2=data[:,1]
r2=data[:,0]

f=numpy.zeros((int(len(f2)),1))
r=numpy.zeros((int(len(r2)),1))


for i in range(0,len(f)):
    f[i]=f2[i]
    r[i]=r2[i]


f= ((N*(N-1))/2) * f/sum(f)

data2=numpy.zeros((len(f),2))

for i in range(0,len(f)):
    data2[i,0]=r[i]
    data2[i,1]=f[i]


print(sum(f))
numpy.savetxt(new_file,data2)

