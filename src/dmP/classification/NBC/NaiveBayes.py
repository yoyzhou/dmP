'''
Created on Oct 5, 2012

@author: yoyzhou
'''
import math
from utils.DataSource import DataSource

class NaiveBayes(object):
    '''
    Naive Bayes Classifier
    '''

    def __init__(self, datafile):
        '''
        Constructor:
        @param  datafile: training set
        '''
        self.datasource = DataSource(datafile)
        
        
    def classify(self, contAttrs = [], **kwargs):
        """"
        Classify test sample/set using NB classifier
        @param contAttrs: specify the continual attributes in test sample/set
        @param kwargs: attribute-value pair or test set, once testset=... is given, only test set is used 
        """
        
        clazzes = self.datasource.getClasses()

        testset = []
        if "testset" in kwargs.keys():
            testset = kwargs["testset"]
        else:
            testset.append(kwargs)
        
        prob = 0.0
        clazzProb = []
        
        for record in testset:
            prob = 0.0
            clazzProb = []
            for clss in clazzes:
                attrval = {}
                attrval[self.datasource.targetAttr] = clss
                prob = self.probD(self.datasource.dataset, attrval)
                
                for attr, value in record.items():
                    if attr == self.datasource.targetAttr:
                        continue
                    
                    attrval = {}
                    attrval[attr] = value
                    if attr in contAttrs:
                        prob *= self.conditionalEstimation(clss, attrval, continual = True)
                    else:
                        prob *= self.conditionalEstimation(clss, attrval, continual = False)
                
                clazzProb.append([clss, prob])
            
            classlabel = [c[0] for c in clazzProb if c[1] == max(p[1] for p in clazzProb)][0]
            
            record['?'] = classlabel
        
        
        
    def probD(self, dataset, attrvalDict=None, **kwargs): 
        """"
            Calculate  probability for DISCRETE Attributes.
        """
        
        totalrecords = len(dataset)        #Total number of records           
        
        attrmatch = 0                           #Determine whether record meet the attribute(s) condition
        matchrecords = 0                     #Number of records which match the attribute(s) condition 
        
        for record in dataset:
            
            if not attrvalDict:
                attrvalDict = kwargs
                 
            for k , v in attrvalDict.items():
                if record[str(k)] == v:
                    attrmatch += 1
                    
            #If number of attributes, which match condition, equals conditions' length, 
            #then record matches  attribute conditions
            if attrmatch == len(attrvalDict): 
                matchrecords += 1
        
        #return matchrecords * 1.0 / totalrecords
        return  (matchrecords * 1.0 + 3 * 1.0 /3 ) /  ( totalrecords + 3)
    
    def probC(self, dataset, attrvalDict=None, **kwargs): 
        """"
            Calculate  probability for CONTINUAL Attributes.
            For sure kwargs only contains one attribute-value pair, if not, only the first pair  (but not guaranteed) will be used
        """
        
        if not attrvalDict:
            attrvalDict = kwargs
                
        attrname, value = attrvalDict.popitem()
        
        v_seq = [int(v[attrname]) for v in dataset]
        
        n = len(v_seq)
        seq_mean = sum(v_seq) * 1.0 / n
        seq_std = math.sqrt(sum((x - seq_mean)**2 for x in v_seq) / n)
        
        estimate = (1.0 / (math.sqrt(2 * math.pi) * seq_std)) * math.exp(-1 * (int(value) - seq_mean)**2 / (2.0 * seq_std **2))
        
        
        return estimate
    
    
    def conditionalEstimation(self, condition, attrvalDict=None, continual = False, **kwargs):
        """
        Estimates probability of attribute(s) under condition of certain class
        Note this method only suitable for DISCRETE attributes
        @param condition: certain class label 
        @param continual: True for continual attribute, the default value is False
        @param **kwargs: key-value pair of attribute(s) being estimated
        @return: conditional probability for attribute(s)
        """
        
        dataset = self.datasource.subDataSet(self.datasource.dataset, self.datasource.targetAttr, condition)
        if continual:
            return self.probC(dataset, attrvalDict, **kwargs)
        else:
            return self.probD(dataset, attrvalDict, **kwargs)
    
        
    def evidence(self, attrvalDict=None, **kwargs):
        """"
        Calculate evidence of attribute(s) condition
        Note for if kwargs contains continual attribute then evidence is not a appropriate measurement 
        when training sample is small, but for large training set, calculate evidence for continual attribute is reasonable. 
        """
        return self.probD(self.datasource.dataset, attrvalDict, **kwargs)
        