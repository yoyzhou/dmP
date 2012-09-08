'''
Created on Sep 2, 2012

@author: yoyzhou
'''
import unittest
from dmP.classification.dtree import DecisionTree

from dmP.classification.id3 import splitor


class TestClassification(unittest.TestCase):


    def setUp(self):
        self.datafile = '../data1'
        self.dtree = DecisionTree(self.datafile, splitor)
        

    def testDecisionTree(self):
        """
        """
        self.dtree.createDecisionTree().prettyTree()
        
        self.dtree.makeDecision(testfile = self.datafile)
        
    def tearDown(self):
        pass
        
if __name__ == "__main__":

    unittest.main()