#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Python/pyROOT macro for training classifiers on a dataset.
#    Specify input, training variables, etc. in top of script before running in shell.
#    Weights are stored in ./weights[title]: 
#    Validation data stored in: ./[outpath].root 
#    TMVA Manual http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf '''
#
#  Original by:
#  Authors: Lars Egholm Pedersen & Troels Petersen (NBI)
#  Date: 7th of January 2016
#
#  Modified by:
#  Author: Johannes Bellm
# ----------------------------------------------------------------------------------- #

import ROOT


# ------------------------------------------------------------
# Setup input and training parameters here

# The variables defined in varlist should also be checked to match the input files headers
title   = "TMVAClassification"
outpath = "TMVAClassification.root"

sigpath = "./Signal.txt"
bkgpath1 = "./Background1.txt"
bkgpath2 = "./Background2.txt"

crossSectionSignal=1.
crossSectionBackground1=1.
crossSectionBackground2=1.


# Define list of variables that will be trained on ( , "f") is there to tell TMVA that it is a 
# floating point number. Use I for integers (descrete variables)
varlist = [ ("x", "f"),
            ("y", "f") ]


methodlist = [ (ROOT.TMVA.Types.kFisher, "Fisher", "") ,
               (ROOT.TMVA.Types.kBDT, "BDTA", ":".join([
                "NTrees=100","MinNodeSize=7","MaxDepth=7","BoostType=AdaBoost","AdaBoostBeta=0.5",
                "SeparationType=GiniIndex","nCuts=20","PruneMethod=NoPruning"])) ]


# ------------------------------------------------------------
# Section for setting up TMVA

# ROOT file that will store TMVA validation data
tmvaoutput = ROOT.TFile( outpath, "RECREATE" )

factory = ROOT.TMVA.Factory( title, tmvaoutput, 
                             ":".join([ "!V",                            # Dont print everything
                                        "!Silent",                         # Print something
                                        "Transformations=I",               # Perform training on dataset without transforming
                                        "AnalysisType=Classification"] ) ) # Analysis is of 'A vs B' separation type

dataloader = ROOT.TMVA.DataLoader()

# Connect TMVA factory to input:
#dataloader.SetInputTrees( sigpath, bkgpath )


# Register the trees
dataloader.AddSignalTree    ( sigpath,  crossSectionSignal );
dataloader.AddBackgroundTree( bkgpath1, crossSectionBackground1 );
dataloader.AddBackgroundTree( bkgpath2, crossSectionBackground2 );

# Add variables:
for ivar in varlist :
    # Arguments :           name     title    data-type
    dataloader.AddVariable( ivar[0], ivar[0], ivar[1] );
    dataloader.SetWeightExpression("weight")


dataloader.PrepareTrainingAndTestTree(ROOT.TCut(""), ROOT.TCut(""),   # No cuts needed due to multiple files.
                                    ":".join([ "nTrain_Signal=0",     # Number of signal events used, 0 = ALL
                                               "nTrain_Background=0", # Number of background events, 0 = ALL
                                               "SplitMode=Random",    # How are events chosen to be used for either training or testing
                                               "NormMode=None",       # Integral of datasets is given by number of events
                                                                      #   (could e.g. also be sum of weights or simply defined to be 1)
                                               "!V"                   # Don't print everything (i.e. not verbose) 
                                               ]))

# Tell TMVA which types of classifiers it should try out (i.e. the ones specified in methodlist)
for imeth in methodlist : 

    # Arguments                    type      name      options
    factory.BookMethod(dataloader, imeth[0], imeth[1], imeth[2] )

# Perform training
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

# Close opened files
tmvaoutput.Close()



# This will open the Gui where you can examine the classifier behaviour
# this can also be done later by : 


ROOT.TMVA.TMVAGui( outpath )


raw_input( ' Press any key to exit ' )
