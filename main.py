#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 15:59:25 2017

@author: zhenshan
"""
# Add function/data folder into module searching path
import sys
import os
sys.path.append(os.getcwd() + '/function')
sys.path.append(os.getcwd() + '/data')
import pandas as pd
# import Self defined module
import FeatureGeneration
import load
import Visualization
import DataManipulation


#==============================================================================
# Data Loading(pandas trunk & HDF5)
#==============================================================================
sentenceTrain = load.loadOrderedSentence()# sentence in order of Ecog data
ecogTrain = load.loadEcog()# Ecog data
rawIntervals = load.loadPhone() # raw split point data 

#==============================================================================
# Data Scaling(Parallelized)
#==============================================================================
ecogTrainScaled = DataManipulation.ScalingBySilence(ecogTrain, rawIntervals)

#==============================================================================
# Feature Generation
#==============================================================================
# parameters
featureList = ['mean']
nodeIdx = [0] # start from 0 to 69(70 in total)
frequency = ['Delta', 'Theta', 'Alpha' ,'Beta' ,'Low Gamma', 'High Gamma']# ['Delta', 'Theta', 'Alpha' ,'Beta' ,'Low Gamma', 'High Gamma']

# Generation
featureDF = FeatureGeneration.FeatureDF(ecogTrainScaled, sentenceTrain, nodeIdx, frequency, featureList, rawIntervals)
featureDF = featureDF.dropna()# Remove observations with nan

#==============================================================================
# Data Visualization
#==============================================================================
n_neighbors = 10
n_components = 2

X = featureDF.ix[:,1:7]

color = pd.DataFrame(featureDF.ix[:,"phone name"].astype('category'))
cat_columns = color.select_dtypes(['category']).columns
color[cat_columns] = color[cat_columns].apply(lambda x: x.cat.codes)

Visualization.DimensionReduction(n_neighbors, n_components, X, color)