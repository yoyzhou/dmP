'''
Created on Sep 6, 2012

@author: yoyzhou
'''
import unittest
from utils.DataSource import DataSource

class Test(unittest.TestCase):


    def setUp(self):
        self.datafile = '../data'
        self.ds = DataSource(self.datafile)

    def testInitialization(self):
        ds = DataSource('../data')
        self.assertEqual(ds.targetAttr, 'Purchase?')
        self.assertEqual(len(ds.dataset), 20)
        self.assertEqual(ds.datafile, self.datafile)
        
    def testInitialization2(self):
        ds = DataSource('../data', 'Purchase?')
        self.assertEqual(ds.targetAttr, 'Purchase?')
        self.assertEqual(len(ds.dataset), 20)
        self.assertEqual(ds.datafile, self.datafile)
    
    def testMojorityValue(self):
        self.assertEqual(self.ds.majorityValue('Purchase?'),'will buy')
    
    def tearDown(self):
        del self.ds
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()