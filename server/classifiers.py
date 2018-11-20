# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 06:36:21 2018

@author: AAS
"""

import threading
import feature_selection as feature_selection

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

rfe_et = None
rfe_knn = None
rfe_dt = None
rfe_rf = None

def run_extra_trees_classifier(X, y):
    print('---------------EXTRA TREES CLASSIFIER RUNNING-------------------------')
    # TODO - Have to decide on which solver to use
    #estimator_log = LogisticRegression(multi_class='multinomial', solver='newton-cg')
    estimator_et = ExtraTreesClassifier(n_estimators = 10, random_state = 0)
    global rfe_et
    rfe_et = feature_selection.perform_RFECV(estimator_et, X, y)
    print('---------------EXTRA TREES CLASSIFIER FINISHED WITH SCORE = -------------------------', rfe_et.score(X,y))
    
def run_k_nearest_neighbors(X, y):
     print('---------------K NEAREST NEIGHBORS START-------------------------')
     estimator_knn = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
     global rfe_knn
     rfe_knn = feature_selection.perform_RFECV(estimator_knn, X, y)
     print('---------------K NEAREST NEIGHBORS END-------------------------')
     
def run_naive_bayes(X, y):
     print('---------------NAIVE BAYES START-------------------------')
     estimator_knn = GaussianNB(n_neighbors = 5, metric = 'minkowski', p = 2)
     global rfe_knn
     rfe_knn = feature_selection.perform_RFECV(estimator_knn, X, y)
     print('---------------NAIVE BAYES START-------------------------')
    
def run_decision_tree(X, y):
    print('---------------DECISION TREE ALGORITHM RUNNING -------------------------')
    estimator_dt = DecisionTreeClassifier(criterion='entropy', random_state = 0)
    global rfe_dt
    rfe_dt = feature_selection.perform_RFECV(estimator_dt, X, y)
    print('---------------DECISION TREE FINISHED WITH SCORE = -------------------------', rfe_dt.score(X,y))
    
def run_random_forest(X, y, num_trees):
    print('---------------RANDOM FOREST(', num_trees,' trees) RUNNING-------------------------')
    estimator_rf = RandomForestClassifier(n_estimators = num_trees, criterion='entropy', random_state = 0)  
    global rfe_rf
    rfe_rf = feature_selection.perform_RFECV(estimator_rf, X, y)
    print('---------------RANDOM FOREST(', num_trees,' trees) FINISHED WITH SCORE = -------------------------',rfe_rf.score(X,y) )

"""def run_SVC(X, y):
    print('---------------SVC START-------------------------')
    estimator_svc = SVC(kernel='linear')
    rfe = perform_RFECV(estimator_svc, X, y)
    print('---------------SVC END-------------------------')
    return rfe"""

def run_classifiers(X, y):
    t1 = threading.Thread(target=run_decision_tree, args=(X, y))
    t2 = threading.Thread(target=run_random_forest, args=(X, y, 10))
    t3 = threading.Thread(target=run_extra_trees_classifier, args=(X, y))
    
    t1.start()
    t2.start()
    t3.start()
    
    t1.join()
    t2.join()
    t3.join()
    
    rfe_scores = {}
    rfe_scores[rfe_dt.score(X, y)] = rfe_dt
    rfe_scores[rfe_rf.score(X, y)] = rfe_rf
    rfe_scores[rfe_et.score(X, y)] = rfe_et
    
    rfe_scores_sorted = sorted(rfe_scores.items(), key=lambda s: s[0], reverse=True)    
    #print('rfe_scores_sorted by score = ', rfe_scores_sorted)
    
    return rfe_scores_sorted[0][1]