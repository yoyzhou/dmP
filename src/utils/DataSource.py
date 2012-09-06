'''
Created on Sep 6, 2012

@author: yoyzhou
'''

class DataSource(object):
    '''
    Class handling data set
    '''


    def __init__(self, datafile, targetAtrr = None):
        '''
        DataSource constructor.
        @param datafile: data set file which follows csv format
        @param targetAtrr: target/feature attribute name, by default it's will be the last attribute of data set  
        '''
        
        self.datafile = datafile
        try:
            datastream = open(self.datafile, 'r')
        except IOError:
                raise IOError('Cannot open the specified file %s', self.datafile)  
        
        
        lines = [line.strip() for line in datastream.readlines()]
    
        #Create attributes list, for csv file the attributes or named column names are the first line of data file. 
        self.attributes = [attr.strip() for attr in lines[0].split(",")]
        if not targetAtrr:
            self.targetAttr = self.attributes[-1]
        else:
            self.targetAttr = targetAtrr 
        #Delete the first line from data file
        del lines[0]
        
        #Data set property
        self.dataset = []
            
        for line in lines:
            self.dataset.append(dict(zip(self.attributes,
                                         [data.strip() for data in line.split(",")])))
        
        datastream.close()
    
    def majorityValue(self, dataset, attr = None):
        """
         Return the majority value for the specific attribute 
         @param attr: Attribute name
        """
        if not attr:
            attr = self.targetAttr
            
        attrValues = self.getAttrValues(dataset, attr)
        return max(attrValues, key=attrValues.count)
    
    def getAttrValues(self, dataset, attr):
        """
        Return a list of values for the given attribute
        @param attr: the attribute to be fetched
        """
        return [v[attr] for v in dataset]
    
    def bestSplitor(self, attributes, fitness):
        """
        Cycles through all the attributes and returns the attribute with the
        highest information gain (or lowest entropy).
        """

        best_gain = 0.0
        best_attr = None
    
        for attr in attributes:
            gain = fitness(self.dataset, attr, self.targetAttr)
            if (gain >= best_gain and attr != self.targetAttr):
                best_gain = gain
                best_attr = attr
                    
        return best_attr

    def unique(self, dataset, attr):
        """
        Return the unique values of the given attribute
        @param attr: Attribute name
        """
        return set(self.getAttrValues(dataset, attr))
    
    def subDataSet(self, attr, val):
        """
        Return sub data set which attribute <attr> equals <val>, e.g. subDataSet('weather', 'sunny') means return 
        a sub data set which weather is sunny.
        @param attr: retrieved attribute name
        @param val: retrieved value  
        """
        return [ data for data in self.dataset if data[attr] == val ]
        