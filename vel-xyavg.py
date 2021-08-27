#!/usr/bin/env python

# Script to parse and xy-plane average .cube files from QE/Environ output
#
# To use:
# python cube2dat.py filename.cube [outfilename]
#
# Prints data file of form { z , xy-averaged quantity }
#
# Zach Goldsmith, Princeton University 2019

import sys
import re
import math
import os
import numpy as np 

# Constants 
bohr2a=0.5291770000
Ry2eV=13.60565000
b3toa3=bohr2a**3

# Cube and output files 
cube = sys.argv[1] 
if len(sys.argv) > 2:
 plavg = sys.argv[2]
else :
 plavg = "output.dat"

#Gather cube file indices and dimensions 
fcube=open(cube)
lines=fcube.readlines()
natom=[lines[2].split()][0][0]
ndat=len(lines)-int(natom)-6
nx=int([lines[3].split()][0][0]) 
ny=int([lines[4].split()][0][0])
nz=int([lines[5].split()][0][0])
sx=float([lines[3].split()][0][1])*bohr2a 
sy=float([lines[4].split()][0][2])*bohr2a
sz=float([lines[5].split()][0][3])*bohr2a
z=np.linspace(0,sz*(nz-1),nz,endpoint=True)

#Collect, reshape, and average cube data via numpy
cubedat=np.genfromtxt(cube,dtype='float',skip_header=int(natom)+6)
fcube.close()
cubenew=cubedat.reshape((nx,ny,nz))
cubeavg=np.mean(cubenew,axis=(0,1))
np.savetxt(plavg,np.vstack((z,cubeavg*Ry2eV)).T)

#Accomplish via triple-loop (~3x slower)

#Reconstruct 3D data - Generally not needed other than for fancy 3D plotting...memory intensive 
#cubexyz=np.zeros((nx*ny*nz,4))
#l=0
#for i in range(nx):
# for j in range(ny):
#  for k in range(nz):
#   cubexyz[l][0]=i*sx
#   cubexyz[l][1]=j*sy
#   cubexyz[l][2]=k*sz
#   cubexyz[l][3]=cubeflat[i*ny*nz+j*nz+k]*Ry2eV
#   l=l+1

#xy-plane average

# cubeavg=np.zeros((nz,1))
# for k in range(nz):
#  for j in range(ny):
#   for i in range(nx):
#    cubeavg[k]=cubeavg[k]+cubeflat[i*ny*nz+j*nz+k]/nx/ny
# 
# #Write plane-averaged output: { z , data(z)  } 
# fout=open(plavg,"w")
# for k in range(nz):
#  s = "%15.8f %15.8f\n" % (k*sz,cubeavg[k])
#  fout.write(s)
# fout.close()
# 
