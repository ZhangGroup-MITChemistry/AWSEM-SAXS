import sys
import os.path
import math
import random
import numpy as np

# Writes a collective variables file called pdbid.colvars and a alpha file with all 0s for a pr_file called pdbid.pr
# useage: python pr_setup.py pdbid

pdbid=sys.argv[1]

pr_file=pdbid+'.pr'
pr=open(pr_file,'r')
line=pr.readline()
count=0
while line:
    line_split=line.split()
    if len(line_split)>1:
        count=count+1
    line=pr.readline()
pr.close()

colvar_file=pdbid+'.colvars'
f=open(colvar_file,'w')


f.write("colvarsTrajFrequency    100 \n") # Default frequency of output: 100 steps
f.write("colvarsRestartFrequency 100 \n")
f.write("indexFile               groups.ndx \n")
f.write("\n\n")
for i in range(0,count):
    f.write("colvar {\n")
    f.write("name    pr"+str(i)+'\n')
    f.write('prbias {\n atoms {\n indexGroup alpha_carbons\n }\n prbias          true \nPrFile          '+pr_file+'\n')
    f.write("alpha           alpha.txt\n prindex         "+str(i)+"\n")
    f.write("    }\n}\n\n")
for i in range(0,count):
    f.write("linear {\nname              max_ent"+str(i)+'\n')
    f.write("colvars           pr"+str(i)+'\n')
    f.write("centers           0\nforceConstant     1\noutputEnergy      no\n}\n\n")
f.close()

new_file2=alpha.txt
new=open(new_file2,'w')
for i in range(0,count)
    new.write('0\n')
new.close()
