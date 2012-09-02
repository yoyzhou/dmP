'''
Created on Sep 2, 2012

@author: yoyzhou
'''
import unittest
from dmP.classification.dtree import create_decision_tree
from dmP.classification.dtree import classify
from dmP.classification.id3 import gain

import sys

class TestClassification(unittest.TestCase):


    def setUp(self):
        self.trainingfile = '../data'
        self.testfile = '../data'
        
        try:
            self.training = open(self.trainingfile, mode = 'r')
            self.testing = open(self.testfile, mode = 'r')
        except IOError:
            print("Error: The file '%s' was not found on this system."  % self.trainingfile)
            sys.exit(0)

    def testClassification(self):
        """
        """
        
        # Create a list of all the lines in the data file
        lines = [line.strip() for line in self.training.readlines()]
    
        # Remove the attributes from the list of lines and create a list of
        # the attributes.
        attributes = [attr.strip() for attr in lines[0].split(",")]
        del lines[0]
        target_attr = attributes[-1]
    
        # Create a list of the data in the data file
        trainingset = []
        
        for line in lines:
            trainingset.append(dict(zip(attributes,
                                 [data.strip() for data in line.split(",")])))
            
        # Copy the data list into the examples list for testing
        examples = trainingset[:]
        
        # Create the decision tree
        tree = create_decision_tree(trainingset, attributes, target_attr, gain)
    
        # Classify the records in the examples list
        classification = classify(tree, examples)
    
        # Print out the classification for each record
        for item in classification:
            print(item)
        
       
    
    def tearDown(self):
        self.training.close()
        self.testing.close()
        
if __name__ == "__main__":

    unittest.main()