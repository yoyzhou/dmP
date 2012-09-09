'''
Created on Sep 2, 2012

@author: yoyzhou
'''

from pyTree.Tree import Tree
from utils.DataSource import DataSource
 
class DecisionTree(object):
    """
       A Decision Tree Class
    """
    def __init__(self, datafile, splitmetric):
        """
        Constructor:
        @param datafile: training set, path to training data file
        @param splitmetric: fitness metric/function to choose best splitter 
        """
        self.datasource = DataSource(datafile)
        self.splitmetric = splitmetric
        self.decisiontree = None
        
    def createDecisionTree(self):
        """
        Create a decision tree against training set
        """
        self.decisiontree = self.__treeGrowth__(self.datasource.dataset, 
                                                self.datasource.attributes, 
                                                self.datasource.targetAttr)
        return self
    
    def makeDecision(self, sample = None, testset = None, testfile = None ):
        """
        Make decision against test set/sample
        """
        testsamples = []
        if testfile:
            ds = DataSource(testfile)
            testsamples.extend( ds.dataset )
        elif testset:
            testsamples.extend(testset)
        elif sample:
            testsamples.append(sample)
        else:
            raise ValueError('No test set passed in.')
       

        for test in testsamples:
            dtree = self.decisiontree
            while True:
                attr = dtree.data.attribute
                node = dtree.getNode(test[attr], False)
                if node.isBranch():
                    test['decision?'] = node.data.attribute
                    break
                else:
                    dtree = node
                    
            
            print(test)
    
    def prettyTree(self):
        """"
        Print decision tree
        """
        try:
            self.decisiontree.prettyTree()
        except AttributeError:
            raise AttributeError('You havn\'t create decision tree yet, please make sure you have called createDecisionTree.')
        
    def __treeGrowth__(self, dataset, attributes, target):
        """
        Grows decision tree based on training set
        @param dataset: training set
        @param attributes: attribute set, which may contains target attribute
        @param target: target attribute   
        """
        
        #Target values
        tvals = [record[target] for record in dataset]
        
        default = self.datasource.majorityValue(dataset)
    
        # If the data set is empty or the attributes list is empty, return the
        # default value. 
        if not dataset or (len(attributes) - 1) <= 0:
            return Tree(DecisionNode(default))
        
        # If all the records in the data set have the same classification,
        # return that classification.
        elif tvals.count(tvals[0]) == len(tvals):
            return Tree(DecisionNode(tvals[0]))
        else:
            # Choose best attribute to best classify data
            best = self.splitmetric(dataset, attributes, target)
    
            # Create a new decision tree/node with the best attribute
            dtree = Tree(DecisionNode(best))
            
            #Attributes for next iterator, all attributes except already fitted `best` attribute
            attrs = [attr for attr in attributes if attr != best]
            
            # Create a new decision tree/sub-node for each of the values in the
            # best attribute field
            for val in self.datasource.uniqueValues(dataset, best):
                # Create a subtree for the current value under the "best" field
                subtree = self.__treeGrowth__(
                    self.datasource.subDataSet(dataset, best, val),
                    attrs, 
                    target)
    
                # Set decision condition, and add the new subtree
                subtree.data.condition = val  
                dtree.addChild( subtree)
                
    
            return dtree


class DecisionNode(object):
    """
    Class of decision node, owning two members:
        attribute: classifier attribute
        condition: classifier condition
    """
    def __init__(self, attribute, condition = None):
        """
        Constructor: initialize a decision node with classification attribute and condition(by default None).
        """
        self.attribute = attribute
        self.condition = condition
        
    def __str__(self, *args, **kwargs):
        
        return str(self.attribute) + ( ' [' + str(self.condition) + ']' if self.condition else '' )
    
    def __eq__(self, other):
        return str(self.condition) == str(other)