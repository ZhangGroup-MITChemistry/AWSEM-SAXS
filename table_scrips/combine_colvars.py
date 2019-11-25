import sys
import os
import math
import numpy

filenames=[]
for i in range(1,len(sys.argv)):
    filenames.append(sys.argv[i])

new_file='combined_colvars.traj'
new=open(new_file,'w')

for i in range(0,len(filenames)):
    filename=filenames[i]
    f=open(filename,'r')
    line=f.readline()
    while line:
        new.write(line)
        line=f.readline()
    f.close()
new.close()