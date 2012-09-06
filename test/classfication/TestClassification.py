'''
Created on Sep 2, 2012

@author: yoyzhou
'''
import unittest
from dmP.classification.dtree import DecisionTree

from dmP.classification.id3 import gain


class TestClassification(unittest.TestCase):


    def setUp(self):
        self.datafile = '../data'
        self.dtree = DecisionTree(self.datafile, gain)
        

    def testDecisionTree(self):
        """
        """
        self.dtree.createDecisionTree(self.dtree.dataset, self.dtree.attributes).prettyTree()
        
        
       
    
    def tearDown(self):
        pass
        
if __name__ == "__main__":

    unittest.main()