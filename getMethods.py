import ROOT


def getMethods():
    return [ (ROOT.TMVA.Types.kFisher, "Fisher", "") ,
             (ROOT.TMVA.Types.kBDT, "BDTA", ":".join([
		"NTrees=100","MinNodeSize=5","MaxDepth=5",
		"BoostType=AdaBoost","AdaBoostBeta=0.5",
                "SeparationType=GiniIndex","nCuts=20",
		"PruneMethod=NoPruning"])) 
	   ]



def getMethodList():
	return  [ "BDTA", "Fisher" ]

