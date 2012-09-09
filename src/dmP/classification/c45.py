'''
Created on Sep 9, 2012

@author: yoyzhou
'''
from dmP.classification.Splitter import Splitter
from dmP.classification.id3 import ID3
import math

class C45(Splitter):
    '''
    C45 algorithm
    '''
    
    def splitmetric(self, dataset, attr, target_attr):
        """
        Calculate gain ratio for C4.5 algorithm
        """
        freq = {}
        splitinfo = 0.0
        
        #Call information gain
        gain = ID3.splitmetric(self, dataset, attr, target_attr);
        samplenumbers = len(dataset)
        # Calculate the frequency of each of the values in the split attribute
        for record in dataset:
            if (record[attr] in freq):
                freq[record[attr]] += 1.0
            else:
                freq[record[attr]] = 1.0
        
        #Calculate split info, entropy of splitter
        for val in list(freq.values()):
            splitinfo += (- val / samplenumbers) * math.log(val / samplenumbers, 2)
        
        #Split info equals 0 when there only one class in data set
        if splitinfo == 0:
            splitinfo = 0.00000001
            
        return gain / splitinfo 
        
