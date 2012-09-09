'''
Created on Sep 2, 2012

@author: yoyzhou
'''
import unittest
from dmP.classification.dtree import DecisionTree

from dmP.classification.id3 import ID3
from dmP.classification.c45 import C45

class TestClassification(unittest.TestCase):


    def setUp(self):
        self.datafile = '../data'
        self.dtree = DecisionTree(self.datafile, C45().selector)
        

    def testDecisionTree(self):
        """
        """
        self.dtree.createDecisionTree().prettyTree()
        
        self.dtree.makeDecision(testfile = self.datafile)
        
    def tearDown(self):
        pass
        
if __name__ == "__main__":

    unittest.main()