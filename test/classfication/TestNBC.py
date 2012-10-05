'''
Created on Oct 5, 2012

@author: yoyzhou
'''
import unittest
from dmP.classification.NBC.NaiveBayes import NaiveBayes


class Test(unittest.TestCase):


    def setUp(self):
        self.nb = NaiveBayes('../data/loan.csv')
        

    def testClassify(self):
        self.nb.classify(['Taxable Income'], testset = self.nb.datasource.dataset)
        print(self.nb.datasource.dataset)
        
        
    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()