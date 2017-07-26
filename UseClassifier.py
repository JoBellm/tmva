#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Python/pyROOT macro for applying TMVA classifiers on a dataset.
#    Specify input, training variables etc in top of script before running in shell.
#    Assumes that the TrainClassifier.py script has been run first
#
#  Original by:
#  Authors: Lars Egholm Pedersen & Troels Petersen (NBI)
#  Date: 7th of January 2016
#
#  Modified by:
#  Author: Johannes Bellm
#
# ----------------------------------------------------------------------------------- #

import ROOT
from array import array 

# Path prefix to TMVA weight files created by the TrainClassifier.py script
weightprefix = "default/weights/TMVAClassification"

# Specify path to ascii files:
testpath = "./Test.txt"

# Name of variables
varlist = ["x", "y"] 

# Define list of methods that you have trained in the previous script (Given by titles)
methodlist = [ "BDTA", "Fisher" ]
outputx=[]
outputy=[]
outputweight=[]

negoutputx=[]
negoutputy=[]
negoutputweight=[]


# ------------------------------------------------------------
# Section for setting up TMVA weight reader
# ------------------------------------------------------------
reader = ROOT.TMVA.Reader()

# Define a dictionary of variables vardict["name"] = value
vardict = { ivar : array('f', [0.0]) for ivar in varlist }

# Connect variables to reader
for ivar in varlist :
    #                   name, array that will contain values
    reader.AddVariable( ivar, vardict[ivar] )

# Tell the reader which methods you want to use:
for imeth in methodlist :
    # Make sure the weightprefix and method names match whatever is is ./weights
    reader.BookMVA( imeth, weightprefix+"_"+imeth+".weights.xml" )



testtree = ROOT.TTree()
testtree.ReadFile( testpath )

# Connect variables to signal tree
for ivar in varlist :
    testtree.SetBranchAddress( ivar, vardict[ivar] )

for ientry in xrange( testtree.GetEntries() ) :
  
    # Retrieve data and check if valid
    if testtree.GetEntry(ientry) < 0 :
      print "Error reading Signal tree, breaking"
      break
    value=reader.EvaluateMVA( methodlist[0] )
    if value > 0. :
      outputx+=[vardict["x"][0]]
      outputy+=[vardict["y"][0]]
      outputweight+=[value]
    else:
      negoutputx+=[vardict["x"][0]]
      negoutputy+=[vardict["y"][0]]
      negoutputweight+=[-value]

# ----------------------------------------------------------------------------------- #
#  Plot generated data:
# ----------------------------------------------------------------------------------- #
import matplotlib.pyplot as plt
import numpy as np


plt.scatter(np.array(outputx),np.array(outputy),s=np.array(outputweight)
            , color="green", alpha=0.5, lw=0)
plt.scatter(np.array(negoutputx),np.array(negoutputy),s=np.array(negoutputweight)
            , color="red", alpha=0.5, lw=0)
plt.xlim([-9.,9.])
plt.ylim([-5.,5.])
plt.show()

exit()
