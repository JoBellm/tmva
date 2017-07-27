#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Python/pyROOT macro for generating a simple dataset.
#  Execute in shell, which produces output files:
#    - Signal.txt
#    - Background1.txt
#    - Background2.txt
#    - Test.txt
#  Original from:
#  Authors: Lars Egholm Pedersen & Troels Petersen (NBI)
#  Date: 7th of January 2016
#
#  Modified by:
#  Authors: Johannes Bellm
# ----------------------------------------------------------------------------------- #
import ROOT

outprefixSG = "./Signal"
outprefixBG1 = "./Background1"
outprefixBG2 = "./Background2"
npoint = 10000
seed = 1

ROOT.gRandom.SetSeed( seed )
# for background 1 histo:
BG1x=[]
BG1y=[]
BG1w=[]

# for background 2 histo:
BG2x=[]
BG2y=[]
BG2w=[]

# for signal histo:
SGx=[]
SGy=[]
SGw=[]

# ----------------------------------------------------------------------------------- #
# Generate data files:
# ----------------------------------------------------------------------------------- #


# Open Ascii output (with open as ... automatically closes file when exiting block)
with open( outprefixSG+".txt", "w" ) as outtxt :
    # ROOT/TMVA needs to know the data format of the txt file if it is to be used as input,
    # so this has to be written as a header of the .txt file:
    outtxt.write("x_f:y_f:weight\n")

    # Generate 'signal' and 'background' distributions:
    for i in xrange( npoint ):
        if (i % 1000 == 0) : print "  Number of generated points: ", i

        # Generate signal
        data = [ROOT.gRandom.Gaus(1,1), # x
                ROOT.gRandom.Gaus(1,1), # y
                1. ]                     # weight
        # Write to .txt file
        outtxt.write( "%8.4f \t %8.4f  \t %8.4f \n"%(data[0], data[1], data[2]) )
        SGx+=[data[0]]
        SGy+=[data[1]]
        SGw+=[data[2]]
        
with open( outprefixBG1+".txt", "w" ) as outtxt :
    # ROOT/TMVA needs to know the data format of the txt file if it is to be used as input,
    # so this has to be written as a header of the .txt file:
    outtxt.write("x_f:y_f:weight\n")
    
    # Generate 'signal' and 'background' distributions:
    for i in xrange( npoint ):
        # Generate background
        data = [ROOT.gRandom.Gaus(-1,1), # x
                ROOT.gRandom.Gaus(-1,1), # y
                1. ]                  # weight
        # Write to .txt file
        outtxt.write( "%8.4f \t %8.4f \t %8.4f \n"%(data[0], data[1], data[2]) )
        BG1x+=[data[0]]
        BG1y+=[data[1]]
        BG1w+=[data[2]]

with open( outprefixBG2+".txt", "w" ) as outtxt :
    # ROOT/TMVA needs to know the data format of the txt file if it is to be used as input,
    # so this has to be written as a header of the .txt file:
    outtxt.write("x_f:y_f:weight\n")
    
    # Generate 'signal' and 'background' distributions:
    for i in xrange( npoint ):
        # Generate background
        data = [ROOT.gRandom.Gaus(1,2), # x
              ROOT.gRandom.Gaus(-2,0.5), # y
              1. ]                  # weight
    
        # Write to .txt file
        outtxt.write( "%8.4f \t %8.4f \t %8.4f \n"%(data[0], data[1], data[2]) )
        BG2x+=[data[0]]
        BG2y+=[data[1]]
        BG2w+=[data[2]]

with open( "Test.txt", "w" ) as outtxt :
    # ROOT/TMVA needs to know the data format of the txt file if it is to be used as input,
    # so this has to be written as a header of the .txt file:
    outtxt.write("x_f:y_f:weight\n")
    import random
    
    # Generate 'signal' and 'background' distributions:
    for i in xrange( npoint*3 ):
      # Generate background
      data = [-9.+random.random()*18., # x
              -5.+random.random()*10., # y
              1. ]                  # weight
        
      # Write to .txt file
      outtxt.write( "%8.4f \t %8.4f \t %8.4f \n"%(data[0], data[1], data[2]) )




# ----------------------------------------------------------------------------------- #
#  Plot generated data:
# ----------------------------------------------------------------------------------- #
import matplotlib.pyplot as plt
import numpy as np


plt.scatter(np.array(BG1x),np.array(BG1y),s=np.array(BG1w), color="red", alpha=0.5, lw=0)
plt.scatter(np.array(BG2x),np.array(BG2y),s=np.array(BG2w), color="orange", alpha=0.5, lw=0)
plt.scatter(np.array(SGx),np.array(SGy),s=np.array(SGw), color="green", alpha=0.5, lw=0)
plt.show()



