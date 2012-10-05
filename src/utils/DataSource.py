'''
Created on Sep 6, 2012

@author: yoyzhou
'''

class DataSource(object):
    '''
    Class handling data source/set
    '''

    def __init__(self, datafile,  zipattr = True, targetAtrr = None):
        '''
        DataSource constructor.
        @param datafile: data set file which follows csv format
        @param targetAtrr: target/feature attribute name, by default it's will be the last attribute of data set  
        @param zipattr: True will zip attributes with values, results data set likes [{attr1:val1, attr2:val2}, {}...], 
                                where each record is a zipped dict with attr-val pair, True is the default value;
                                if False, data record will not be zipped, results data set likes [[val1, val2,..], []...], where 
                                each record is a list of values, not target attribute is included.
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
        if zipattr:    
            #zip attributes with value by default
            for line in lines:
                self.dataset.append(dict(zip(self.attributes,
                                             [data.strip() for data in line.split(",")])))
        else:
            #note the target attribute must at the last column 
            for line in lines:
                self.dataset.append([data.strip() for data in line.split(",")])
                
        datastream.close()
    
    def majorityValue(self, dataset, attr = None):
        """
         Return the majority value for the specific attribute 
         @param attr: Attribute name, default the target attribute
        """
        if not attr:
            attr = self.targetAttr
            
        attrValues = self.getAttrValues(dataset, attr)
        
        return max(attrValues, key=attrValues.count)
    
    def getClasses(self):
        """
        Get unique classes from data set 
        """ 
        return self.uniqueValues(self.dataset,  self.targetAttr)
        
    def getAttrValues(self, dataset, attr):
        """
        Return a list of values for the given attribute
        @param attr: the attribute to be fetched
        """
        return [record[attr] for record in dataset]
    
    
    def uniqueValues(self, dataset, attr):
        """
        Return a set of the uniqueValues values of the given attribute
        @param attr: Attribute name
        """
        return set(self.getAttrValues(dataset, attr))
    
    def subDataSet(self, dataset, attr, val):
        """
        Return sub data set which attribute <attr> equals <val>, e.g. subDataSet('weather', 'sunny') means return 
        a sub data set which weather is sunny.
        @param attr: retrieved attribute name
        @param val: retrieved value  
        """
        return [ data for data in dataset if data[attr] == val ]
    
    
    def dualization(self, outputfile):
        """
        Transform data set into features vector based record, where each feature can only be 0, means record doesn't 
        own the feature, or 1, means record owns the feature. 
        """
        fv = []                             #features vector, including all features, excepts target attribute
        
        #find all the features
        for attr in self.attributes:
            if attr != self.targetAttr:
                fv.extend(self.uniqueValues(self.dataset, attr))
        
        #clazzes = self.uniqueValues(self.dataset, self.targetAttr)
        #clazzesDict = dict(zip(clazzes, range(len(clazzes))))
        
        #output file
        ofile = open(outputfile, 'w')
        
        #write header
        ofile.write(','.join(fv) + ',' + self.targetAttr + '\n')
        
        for record in self.dataset:
            recordfeatures = []
            values = record.values()
            for f in fv:
                if f in values:
                    recordfeatures.append('1')
                else:
                    recordfeatures.append('0')
            ofile.write(','.join(recordfeatures) + ',' + record[self.targetAttr] + '\n')
        
        ofile.close()
        
            
        