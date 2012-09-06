"""
This module holds functions that are responsible for creating a new
decision tree and for using the tree for data classification.
"""

from pyTree.Tree import Tree
from utils.DataSource import DataSource
 
class DecisionTree(object):
    """
    Decision tree class 
    """
    def __init__(self, datafile, fitness):
        
        self.datasource = DataSource(datafile)
        self.fitness = fitness
        self.targetAttr = self.datasource.targetAttr
        self.dataset = self.datasource.dataset
        self.attributes = self.datasource.attributes
        
    def createDecisionTree(self, dataset, attributes):
        """
        Returns a new decision tree based on the examples given.
        """
        
        #Target values
        tvals = [record[self.targetAttr] for record in dataset]
        
        default = self.datasource.majorityValue(dataset)
    
        # If the data set is empty or the attributes list is empty, return the
        # default value. 
        if not dataset or (len(attributes) - 1) <= 0:
            return Tree(default)
        # If all the records in the data set have the same classification,
        # return that classification.
        elif tvals.count(tvals[0]) == len(tvals):
            return Tree(tvals[0])
        else:
            # Choose the next best attribute to best classify our data
            best = self.datasource.bestSplitor(attributes, self.fitness)
    
            # Create a new decision tree/node with the best attribute
            dtree = Tree(best)
    
            # Create a new decision tree/sub-node for each of the values in the
            # best attribute field
            for val in self.datasource.unique(dataset, best):
                # Create a subtree for the current value under the "best" field
                subtree = self.createDecisionTree(
                    self.datasource.subDataSet(best, val),
                    [attr for attr in attributes if attr != best])
    
                # Add the new subtree to the empty dictionary object in our new
                # tree/node we just created.
                dtree.addChild(subtree)
    
        return dtree