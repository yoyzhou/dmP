'''
Created on Sep 9, 2012

@author: yoyzhou
'''

import math

class Splitter(object):
    '''
    Super class of splitter algorithms, subclass of this class must implement `splitmetric` method
    '''
    
    def selector(self, dataset, attributes, target_attr):
        """
        A selector to select the best classifier attribute for current data set.
        It cycles through all the attributes and returns the attribute with the
        highest split metrics score. 
        """

        best_gain = 0.0
        best_attr = None
    
        for attr in attributes:
            gain = self.splitmetric(dataset, attr, target_attr)
            if (gain >= best_gain and attr != target_attr):
                best_gain = gain
                best_attr = attr
                    
        return best_attr
 
    
    def splitmetric(self, dataset, attr, target_attr):
        """
        Metric for how to split data set, per ID3 algorithm is information gain, per C45 is gain ratio, etc.
        """
        raise NotImplementedError('Subclass should implement this method')
     

    
    def entropy(self, dataset, target_attr):
        """
        Calculates the entropy of the given data set for the target attribute.
        @param  data: data set
        @param target_attr: target attribute  
        """
        freq = {} #A dictionary to counts how many samples for each target classification  
        data_entropy = 0.0
        samplenumbers = len(dataset) #Total number of samplers in data set
         
        #Calculate the frequency of each of the values in the target attribute
        for record in dataset:
            if (record[target_attr] in freq):
                freq[record[target_attr]] += 1.0
            else:
                freq[record[target_attr]] = 1.0
    
        # Calculate the entropy of the data for the target attribute
        for freq in list(freq.values()):
            data_entropy += (-freq/samplenumbers) * math.log(freq/samplenumbers, 2) 
            
        return data_entropy