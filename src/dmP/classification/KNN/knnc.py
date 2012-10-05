'''
Created on Oct 3, 2012

@author: yoyzhou
'''

import math
import itertools

class KNN(object):
    '''
    k-Nearest Neighbor algorithm for classification using Euclidean distance
    '''
    
    def __init__(self, trainingset, queryset, k):
        '''
        Constructor for kNN classifier
        @param trainingset: training set
        @param queryset: query set can be multiple records or just one record
        @param k: k of kNN  
        '''
        
        self.trainingset = trainingset
        self.queryset = queryset
        self.k = k
        
    def classify(self, weighted = False, zeroPrize = 1):
        """"
        Classify query set using KNN classifier
        Classification info will update to query set records will multiple queries are  provided
        Classification info will return if only one query  is provided 
        """
        
        #if the first elements of query set is not a list, then query set is a single record 
        if  not isinstance(self.queryset[0], list):
            nearestk = self.__nearestk__(self.queryset)
            clazzes = [t[1] for t in nearestk]
            if weighted:
                classlabel = self.__weightedvotes__(nearestk, zeroPrize)
            else:
                classlabel = max(clazzes, key = clazzes.count)
            
            self.queryset[-1] = classlabel
            #Classification info will return if only one query  is provided 
            return classlabel
        
        else:
                      
            for query in self.queryset:
                
                nearestk = self.__nearestk__(query)
                clazzes = [t[1] for t in nearestk]
                if weighted:
                    classlabel = self.__weightedvotes__(nearestk, zeroPrize)
                else:
                    classlabel = max(clazzes, key = clazzes.count)
                #classification info will update to query set record will multiple query set provided
                query[-1] = classlabel
        
    
    def __weightedvotes__(self, nearestk, zeroPrize = 1):
        
        keyfunc = lambda t: ( t[1] )
        nearestk.sort(key=keyfunc)
        wclazzes = []
        for clazz, rows in itertools.groupby(nearestk, key = keyfunc):
            wvotes = 0.0
            for r in rows:
                if r[0] == 0:
                    wvotes += zeroPrize
                else:
                    wvotes += 1.0/ r[0]
                        
            wclazzes.append([clazz, wvotes])
            print(wclazzes)
            
        return [c[0] for c in wclazzes if c[1] == max([v[1] for v in wclazzes])][0]
        
    def __nearestk__(self, query):
        """
        Return nearest k records for specific query  
        
        @param query: query record 
        """
        #Only nearest k items will be stored 
        nearestk = [None for i in range(self.k)]
        count = 0
            
        for train in self.trainingset:
                
            dis = self.distanceMetric(train[:-1], query[:-1])
           
            #populate k elements first regardless of their distance
            if count < self.k:
                nearestk[count] = [dis, train[-1]]
                count += 1
            else:
                farthest = self.__maxCurrent__(nearestk)
                #if the current distance is larger than current farthest, 
                #update nearest k list, replace the farthest with current distance
                if dis < farthest[0]:   
                    farthest[0] = dis
                    farthest[1] = train[-1]
        
        return nearestk
    
    def __maxCurrent__(self, nearestK):
        """
        Farthest distance item in current nearest k list
        """
        farthest = nearestK[0]
        
        for top in nearestK:
            if top[0] > farthest[0]:
                farthest = top
        
        return farthest
                
                    
    
    def distanceMetric(self, recordT, recordQ):
        """
        Calculate the distance between two records using Euclidean distance
        @param recordT: record in training set
        @param recordQ: record ready for Querying, a.k.a, record in test set  
        """
        #print(list(zip(recordT, recordQ)))
    
        return math.sqrt(sum([pow((float(t[0]) -float(t[1])),2) for t in list(zip(recordT, recordQ))]))
    