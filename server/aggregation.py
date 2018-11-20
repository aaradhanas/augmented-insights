# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 08:17:31 2018

@author: AAS
"""

import pandas as pd
import insight as insightModule
from model import ChartInfo
from model import AggInfo
import util as util

variance_threshold = 0.2

def calc_values_for_aggregation(data_frame, feature, variance_dict, user_selections=None):
    sum = data_frame.sum()
    avg_percent = (data_frame.mean() / sum) * 100
    df_percent = data_frame.apply(lambda x: util.compute_percentage(x, sum))
    df_percent = df_percent[df_percent.values != 0]
    
    variance = getVariance(df_percent.to_dict().values())         

    #print('calc_values_for_aggregation variance = ', variance)
    if variance >= variance_threshold:
        df_reset_index = pd.concat([data_frame, df_percent], axis = 1).reset_index()
        df_reset_index.columns = [feature, 'Counts', 'Percentage']
    
        values = getValuesOnAverage(df_reset_index, avg_percent, feature, 'Percentage')
        #print('df_reset_index variance = ', variance)
        insights = insightModule.getInsights(df_reset_index, user_selections)
        print('INSIGHT GENERATED FOR ', feature, ': ', insights, '\n')
        aggInfo = getAggInfo(values, insights, feature, feature, avg_percent)
        if variance in variance_dict:
            variance_dict[variance].append(aggInfo)
        else:
            aggInfoList = []
            aggInfoList.append(aggInfo)
            variance_dict[variance] = aggInfoList 
    else:
        print('FEATURE REMOVED: ', feature)
    
    if variance == 0:
        return True
    else:
        return False
    
def get_final_aggregation(data, user_selections):
    variance_dict = {}
    aggs = []
    
    for feature in data.columns.values:
        calc_values_for_aggregation(data[feature].value_counts(), feature, variance_dict, user_selections)
                
    variance_dict = sorted(variance_dict.items(), key=lambda s: s[0], reverse=True)
    #print('variance_dict = ', variance_dict)
    for variance_item in variance_dict:
        if variance_item[1] is not None:
            aggs.extend(variance_item[1])
    return aggs
        

# Construct the chart and insight wrapper object
def getAggInfo(chartData, insights, title, column2, avg = 0):
    aggInfo = AggInfo()
    aggInfo.title = title
    aggInfo.insights = insights

    chartInfo = ChartInfo()
    chartInfo.columnName = column2 
    chartInfo.data = chartData
    chartInfo.data_average = avg
    
    itemSize = len(chartInfo.data)
    if itemSize <= 3:
        chartInfo.type = 'doughnut'
        for key, value in chartData.items():
            if isinstance(value, dict) and len(value) > 2:
                #print('value = ', value)
                chartInfo.type = 'bar'
                break;
    else:
        chartInfo.type = 'horizontalBar'
            
    aggInfo.chart = chartInfo
    return aggInfo

def getValuesOnAverage(df, avg_percent, col1, col2):
    df_above_avg = df[df[col2] > avg_percent]
    df_below_avg = df[df[col2] <= avg_percent]
    
    df_significant = df_above_avg.head(2).append(df_below_avg.tail(3))
    
    df_above_avg.drop(df_above_avg.head(2).index, inplace=True)
    df_below_avg.drop(df_below_avg.tail(3).index, inplace=True)
    
    df_significant = df_significant.append(df_above_avg.head(2).append(df_below_avg.tail(3)))
    
    agg_map = dict()
    for index, row in df_significant.iterrows():
        agg_map[row[col1]] = row[col2]
        
    return agg_map

    

# TODO - The 5 values shown should be the one which show the lowest and highest values which respect to average
def getVariedValues(df1, column1, column2):
    #df1 = data[column1].value_counts().reset_index()
    df1.columns = [column1, column2]
    df1 = df1.sort_values(by = column2, ascending=False)
    df_len = len(df1)
    
    agg_map = dict()
    agg_map[str(df1.iloc[0,:][column1])] = str(df1.iloc[0,:][column2])
    agg_map[str(df1.iloc[df_len - 1,:][column1])] = str(df1.iloc[df_len - 1,:][column2])
    
    mid = int(df_len / 2);
    agg_map[str(df1.iloc[mid,:][column1])] = str(df1.iloc[mid,:][column2])
    
    mid1 = int(0 + mid / 2);
    agg_map[str(df1.iloc[mid1,:][column1])] = str(df1.iloc[mid1,:][column2])
    
    mid2 = int((mid + df_len) / 2);
    agg_map[str(df1.iloc[mid2,:][column1])] = str(df1.iloc[mid2,:][column2])
    
    return agg_map

# Given a set of values, returns the variance
def getVariance(feature_values):
    max_value = max(feature_values)
    min_value = min(feature_values)
    #print('max_value = ', max_value)
    #print('min_value = ', min_value)
    variance = (max_value - min_value)/(max_value + min_value)
    return variance