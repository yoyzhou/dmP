"""
This module contains the functions for calculating the information infogain of a
data set as defined by the ID3.
"""

import math

def entropy(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    val_freq = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attribute
    for record in data:
        if (record[target_attr] in val_freq):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in list(val_freq.values()):
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return data_entropy
    
def infogain(dataset, attr, target_attr):
    """
    Calculates the information gain (reduction in entropy) that would
    result by splitting the data on the chosen attribute.
    """
    val_freq = {}
    subset_entropy = 0.0

    # Calculate the frequency of each of the values in the split attribute
    for record in dataset:
        if (record[attr] in val_freq):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    # Calculate the sum of the entropy for each subset of records weighted
    # by their probability of occurring in the training set.
    for val in list(val_freq.keys()):
        val_prob = val_freq[val] / sum(val_freq.values())
        data_subset = [record for record in dataset if record[attr] == val]
        subset_entropy += val_prob * entropy(data_subset, target_attr)

    # Subtract the entropy of the chosen attribute from the entropy of the
    # whole data set with respect to the target attribute.
    return (entropy(dataset, target_attr) - subset_entropy)

def splitor(dataset, attributes, target_attr):
        """
        Cycles through all the attributes and returns the attribute with the
        highest information gain (or lowest entropy).
        """

        best_gain = 0.0
        best_attr = None
    
        for attr in attributes:
            gain = infogain(dataset, attr, target_attr)
            if (gain >= best_gain and attr != target_attr):
                best_gain = gain
                best_attr = attr
                    
        return best_attr
