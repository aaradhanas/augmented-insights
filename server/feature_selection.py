# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:22:39 2018

@author: AAS
"""

from datetime import datetime

distribution_threshold = 50
    
def perform_RFECV(estimator, X, y):
    from sklearn.feature_selection import RFECV    
    rfe = RFECV(estimator = estimator, step=1, cv=3, scoring = 'accuracy')
    
    #start_time = datetime.utcnow()
    rfe = rfe.fit(X, y)
    #end_time = datetime.utcnow()
    #print('Recursive feature elimination completed in ', (end_time - start_time).total_seconds(), ' seconds')

    return rfe

def perform_feature_pruning(rfe_support, dataset_encoded, data_set, delete_in_agg):
    prune_feature_distribution = {}
    global data
    global data_for_agg
    
    for idx, val in enumerate(rfe_support):
        if not val:
            f_prune = dataset_encoded.iloc[:, idx].name
            print('Feature to be pruned : ', f_prune)
            if f_prune in data.columns.values:
                del data[f_prune]
                print('Feature pruned directly: ', f_prune)
                if delete_in_agg:
                    del data_for_agg[f_prune]
            else:
                f_prune = f_prune.split('_')[0]
                if f_prune in prune_feature_distribution:
                    prune_feature_distribution[f_prune] = prune_feature_distribution[f_prune] + 1
                else:
                    prune_feature_distribution[f_prune]  = 1
              
    print('Prune feature distribution = ', prune_feature_distribution)
    # Based on the distribution of categorical variable, prune the feature
    for feature in prune_feature_distribution:
        num_categories = len(data_set[feature].value_counts())
        print('Feature :', feature, ' = ', prune_feature_distribution[feature],
              ' in ', num_categories, " categories")
        dist_percent = (prune_feature_distribution[feature] / num_categories)  * 100
        print('Feature :', feature, ' = ', dist_percent, "%")
        if dist_percent > distribution_threshold:
            del data[feature]
            print('Feature pruned after considering distribution: ', feature)
            if delete_in_agg:
                    del data_for_agg[feature]