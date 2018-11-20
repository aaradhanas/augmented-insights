# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 08:23:39 2018

@author: AAS
"""

import pandas as pd
from datetime import datetime
import dateutil.parser
import json

def compute_percentage(x, sum):
    return round((x / int(sum)) *100, 2)

def read_data_from_file(fileName):
    data = pd.DataFrame()
    filesList = fileName.split(',')
    print('filesList = ', filesList)
    
    if len(filesList) > 0:
        data = pd.read_csv('static/'+filesList[0], encoding = "ISO-8859-1")
        if len(filesList) > 1:
            filesList.remove(filesList[0])
            for file in filesList:
                df = pd.read_csv('static/'+file, encoding = "ISO-8859-1")
                data = pd.merge(data, df)
    return data

def read_data_from_json_file(file_name):
    with open('static/'+file_name) as data_file:
        file_content = json.load(data_file)
    return pd.DataFrame(file_content)

def transformDateColumn(data):
    # Take the column which contains 'Date' as column name
    col = 'Date'
    
    if col not in data.columns.values:
        return data
    
    daysArray = []
    monthsArray = []
    yearsArray = []
    
    for date in data[col]:
        objDate = dateutil.parser.parse(str(date))
        formattedDate = datetime.strftime(objDate, '%d/%b/%Y')
        day, month, year = formattedDate.split('/')
        daysArray.append(day)
        monthsArray.append(month)
        yearsArray.append(year)
    
    data[col+'_Day'] = daysArray
    data[col+'_Month'] = monthsArray
    data[col+'_Year'] = yearsArray

    del data[col]
       
    return data