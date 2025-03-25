# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 13:35:15 2018

@author: Administrator
"""

from Cal_Entropy import cal_entropy  # Corrected import statement

def Split_Data(dataset, axis, value):
    """
    Splits the dataset based on the given axis (feature) and value.

    Args:
        dataset: The dataset to split.
        axis: The index of the feature to split on.
        value: The value of the feature to split on.

    Returns:
        A new dataset containing only the instances where the feature at the
        given axis has the specified value.
    """
    new_subset = []
    for vec in dataset:
        if vec[axis] == value:
            feature_split = vec[:axis]
            feature_split.extend(vec[axis + 1:])
            new_subset.append(feature_split)
    return new_subset

def Split_by_entropy(dataset):
    """
    Splits the dataset based on the feature with the highest information gain.

    Args:
        dataset: The dataset to split.

    Returns:
        The index of the feature that provides the best split according to
        information gain.
    """
    feature_num = len(dataset[0]) - 1
    ent_old = cal_entropy(dataset)
    best_gain = 0.0
    best_feature = -1

    for i in range(feature_num):
        feature_list = [x[i] for x in dataset]
        uniVal = set(feature_list)
        ent_new = 0.0

        for value in uniVal:
            sub_set = Split_Data(dataset, i, value)
            prob = len(sub_set) / float(len(dataset))
            ent_new += prob * cal_entropy(sub_set)  # Corrected entropy calculation

        Info_gain = ent_old - ent_new
        if Info_gain > best_gain:
            best_gain = Info_gain
            best_feature = i

    return best_feature