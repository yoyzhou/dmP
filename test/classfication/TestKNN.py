'''
Created on Oct 3, 2012

@author: yoyzhou
'''
import unittest
from dmP.classification.KNN.knnc import KNN
from utils.DataSource import DataSource


class Test(unittest.TestCase):


    def setUp(self):
        self.ds =DataSource('../data.o', False)
        
        self.knn = KNN(self.ds.dataset[:-2], self.ds.dataset[7], 4)


    def tearDown(self):
        pass

    def testDistanceMetric(self):
        self.assertEqual(self.knn.distanceMetric([0,4,6], [0,1,2]), 5)
        
    def testClassfySingle(self):
        self.knn = KNN(self.ds.dataset[:-2], self.ds.dataset[7], 4)
        self.assertEqual(self.knn.classify(True,3),'will buy')
        #self.knn.classify();
        #print([rtn for rtn in self.knn.queryset]) self.knn = KNN(self.ds.dataset[:-2], self.ds.dataset[7], 4)
    
    def testClassfyMultiple(self):
        self.knn = KNN(self.ds.dataset[3:], self.ds.dataset[0:3], 4)
        self.knn.classify(True, 3);
        print([rtn for rtn in self.knn.queryset])
        
    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()