import chart as chartModule
from model import ChartInfo
from model import AggInfo
from model import MyEncoder
import json

def getChartsAndInsights(fileNames):
    aggs = chartModule.get_level1_data(fileNames)
    aggsEncoded = []

    for aggInfo in aggs:
        aggInfoEncoded = json.dumps(aggInfo, cls=MyEncoder)
        aggsEncoded.append(aggInfoEncoded)
    
    return aggsEncoded

def getCharts(column, value, level):

    if level == '2':
        aggs = chartModule.get_level2_data(column, value)
    else:
        aggs = chartModule.get_level3_above_data(column, value)

    #print("getChartsAndInsights :: ",column," = ", aggs)
    aggsEncoded = []

    for aggInfo in aggs:
        aggInfoEncoded = json.dumps(aggInfo, cls=MyEncoder)
        aggsEncoded.append(aggInfoEncoded)
    
    return aggsEncoded

def generate_pmml_and_deploy():
    chartModule.generate_pmml_from_model()
    # TODO deploy to zementis

"""if __name__ == '__main__':
    getChartsAndInsights()"""
