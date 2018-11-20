# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:50:47 2018

@author: AAS
"""

import pandas as pd
import os
from collections import OrderedDict
from sklearn.preprocessing import LabelEncoder
from nyoka import skl_to_pmml
from sklearn.pipeline import Pipeline

import aggregation as aggregationModule
import classifiers as classifiers
import util as util

variance_thershold = 0.2
data = pd.DataFrame()
data_for_agg = pd.DataFrame()

target_feature = ""
target_value = ""

user_selections = OrderedDict()

X = None
y = None
estimator = None

# For numeric ranges
# np.arange(min(val_num), max(val_num), 5)

# Level 1 charts - Aggregation of all relevant columns
def get_level1_data(fileName):
    print('============================ LEVEL 1 ====================================')

    global data
    if fileName.endswith('.csv'):
        data = util.read_data_from_file(fileName)
    else:
        data = util.read_data_from_json_file(fileName)
        
    data.isnull().any()
    data.fillna(value=0, axis=1, inplace=True)
    
    #data = util.transformDateColumn(data)

    # Aggregation of columns
    variance_dict = {}
    features = data.columns.values
    for f in features:
        fValue = data[f][0]
        
        # By default, round off float to integers
        if isinstance(fValue, float):
            data[f] = round(data[f])
            
        feature_removal = aggregationModule.calc_values_for_aggregation(data[f].value_counts(), f, variance_dict)
        if feature_removal:
            del data[f]
           
    variance_dict = sorted(variance_dict.items(), key=lambda s: s[0], reverse=True)
    
    #print('variance_dict = ', variance_dict)
    
    aggs = []
    for varianceAgg in variance_dict:
        aggs.extend(varianceAgg[1])

    return aggs


"""
LEVEL 2
Step 1: Take into account the target variable (for model) and value (for aggregation)
Step 2: Run feature selection
Step 3: Prune the features which do not influence the target variable
Step 4: Perform aggregation between the influential columns and target variable (Make sure to filter the dataset based
on the value of target variable).
"""
def get_level2_data(column, value):
    #print('get_level2_data')
    print('============================ LEVEL 2 ====================================')
    print('User selection: ', column, ' = ', value)
    global user_selections
    user_selections = OrderedDict()
    user_selections[column] = value
    # Set the target feature on which the model will be created
    global target_feature
    target_feature = column
    # Set the target feature value on which aggregation will be performed
    global target_value
    target_value = value
    
    global X, y
    y = data[target_feature].values
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    
    data_drop_y = data.copy(deep=True)
    del data_drop_y[target_feature]
    
    dataset_encoded = pd.get_dummies(data_drop_y, drop_first=True)
    X = dataset_encoded.iloc[:, :].values
    X = perform_feature_scaling(X)
    
    #print('Training dataset size = ', len(data_drop_y))
    
    rfe = classifiers.run_classifiers(X, y.ravel())
    #print('RFE support vector = ', rfe.support_)
    global estimator 
    estimator = type(rfe.estimator)
    print('ALGORITHM CHOSEN IS ', estimator)
    
    data_level = data.copy(deep=True)
    #print('Before prune = ', data_level.columns.values)
    perform_feature_pruning(rfe.support_, dataset_encoded, data_level, False)
    #print('After prune = ', data_level.columns.values)
    
    #global data_for_agg
    #print('data before = ', data)
    data_for_agg_level = data_level[data_level[target_feature] == target_value]
    del data_for_agg_level[target_feature]
    #print('data_for_agg after = ', data_for_agg)
    return aggregationModule.get_final_aggregation(data_for_agg_level, user_selections)

"""
LEVEL 3 and ABOVE
Step 1: Filter the dataset based on the selected column value
Step 2: Run feature selection
Step 3: Prune the features which do not influence the target variable
Step 4: Perform aggregation on the value of selected column and other values (Make sure to filter the dataset based
on the value of target variable).
"""
def get_level3_above_data(column, value):
    print('============================ LEVEL 3 ====================================')
    print('User selection: ', column, ' = ', value)
    global user_selections
    user_selections[column] = value
    
    global data
    #print('target_feature = ', target_feature)
    data_column_filter = data.copy(deep=True)
    #print('Training dataset size before = ', len(data_column_filter))
    for selection in user_selections.items():
        if selection[0] != target_feature:
            data_column_filter = data_column_filter[data_column_filter[selection[0]] == selection[1]]
            del data_column_filter[selection[0]]
    
    data_level = data_column_filter.copy(deep=True)
    y = data_column_filter[target_feature].values
    del data_column_filter[target_feature]
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    
    dataset_encoded = pd.get_dummies(data_column_filter, drop_first=True)
    X = dataset_encoded.iloc[:, :].values
    X = perform_feature_scaling(X)

    #print('Training dataset size = ', len(data_column_filter))    
   
    rfe = classifiers.run_classifiers(X, y)
    print('ALGORITHM CHOSEN IS ', type(rfe.estimator))
    #print('Before prune = ', data_level.columns.values)
    perform_feature_pruning(rfe.support_, dataset_encoded, data_level, True)
    #print('After prune = ', data_level.columns.values)
    
    data_for_agg_level = data_level[data_level[target_feature] == target_value]
    del data_for_agg_level[target_feature]
    
    #print('data_for_agg before = ', data_for_agg)
    #data_for_agg = data_for_agg[data_for_agg[column] == value]
    #del data_for_agg[column]
    #print('data_for_agg after = ', data_for_agg)
    #print('FEATURES CHOSEN = ', data_for_agg_level.columns.values)
    return aggregationModule.get_final_aggregation(data_for_agg_level, user_selections)


def perform_feature_scaling(feature_vector):
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    feature_vector = sc.fit_transform(feature_vector)
    return feature_vector

def perform_feature_pruning(rfe_support, dataset_encoded, dataset, delete_in_agg):
    prune_feature_distribution = {}
    
    for idx, val in enumerate(rfe_support):
        if not val:
            f_prune = dataset_encoded.iloc[:, idx].name
            #print('Feature to be pruned : ', f_prune)
            if f_prune in dataset.columns.values:
                del dataset[f_prune]
                #print('Feature pruned directly: ', f_prune)
            else:
                f_prune = f_prune.split('_')[0]
                if f_prune in prune_feature_distribution:
                    prune_feature_distribution[f_prune] = prune_feature_distribution[f_prune] + 1
                else:
                    prune_feature_distribution[f_prune]  = 1
              
    #print('Prune feature distribution = ', prune_feature_distribution)
    # Based on the distribution of categorical variable, prune the feature
    for feature in prune_feature_distribution:
        num_categories = len(dataset[feature].value_counts())
        #print('Feature :', feature, ' = ', prune_feature_distribution[feature],' in ', num_categories, " categories")
        dist_percent = (prune_feature_distribution[feature] / num_categories)  * 100
        #print('Feature :', feature, ' = ', dist_percent, "%")
        if dist_percent > 70:
            del dataset[feature]
            print('FEATURE REMOVED: ', feature)
            
            
def generate_pmml_from_model():
    global X, y, estimator

    model_deploy_pipline = Pipeline([("model", estimator())])
    model_deploy_pipline.fit(X,y)
    
    if not os.path.exists('./models'):
        os.makedirs('./models')
            
    skl_to_pmml(model_deploy_pipline, X, y, './models/model.pmml')