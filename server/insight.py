# Module for insight generation

import requests
import pandas as pd
import numpy as py
from model import MyEncoder
from nlgmodel import Sentence
from nlgmodel import Phrase
from nlgmodel import Feature
import json

def build_phrase(coordinates):
    phrase = Phrase()
    phrase.type= 'coordinated_phrase'
    phrase.coordinates=[]
    phrase.coordinates.extend(coordinates)
    return phrase

def build_feature():
    feature = Feature()
    feature.tense = 'present'
    return feature

def get_context(context):
    sentence = Sentence()
    sentence.subject= build_phrase(context)
    return sentence

def get_sentence_payload(subject, verb, object):
    sentence = Sentence()
    #creating subject
    sentence.subject = build_phrase([subject])

    #creating verb
    sentence.verb = verb
    
    #creating object
    sentence.object = build_phrase([object])

    #creating tense type
    sentence.feature = build_feature()

    return sentence


def nlg_service(payload):
    
    sentence_payload = json.dumps({"sentence": payload}, cls=MyEncoder)
    url='http://localhost:8002/generateSentence'
    response = requests.post(url, data=sentence_payload,
                             headers={"Content-Type": "application/json"})
    #print("Insights response:", response.text)
    return response.text

def get_max_insight(dataframe):
    columns = dataframe.columns.values
    maximum = dataframe.loc[dataframe[columns[1]].idxmax()]
    line_count = dataframe.shape[0]

    subject =  '<span class="bold">'+ str(maximum[columns[0]])+'</span>'
    object = 'maximum (<span class="bold number">'+str(maximum[columns[1]])+'%</span>)'
    payload = get_sentence_payload(subject, 'be', object)
        
    created_sentence = nlg_service(payload)
    
    return created_sentence

def get_min_insight(dataframe):
    columns = dataframe.columns.values
    minimum = dataframe.loc[dataframe[columns[1]].idxmin()]
    line_count = dataframe.shape[0]

    subject =  '<span class="bold">'+str(minimum[columns[0]])+'</span>'
    object = 'minimum (<span class="bold number">'+str(minimum[columns[1]])+'%</span>)'
    payload = get_sentence_payload(subject, 'be', object)
        
    created_sentence = nlg_service(payload)
    
    return created_sentence

def get_max_min_insight(dataframe):
    print("get_max_min_insight called")
    columns = dataframe.columns.values
    lines = 'Of the '+columns[0]+'s, ' + get_max_insight(dataframe) + 'and ' + get_min_insight(dataframe)
    return lines

def get_average_insight(dataframe):
    columns = dataframe.columns.values
    dataframe['percentage'] = dataframe["Counts"]/dataframe["Counts"].sum() * 100
    dataframe['avg_percentage'] = dataframe["Counts"].mean()/dataframe["Counts"].sum() * 100
    total_avg_percentage = dataframe["Counts"].mean()/dataframe["Counts"].sum() * 100
    positive_group = dataframe[dataframe['percentage']>total_avg_percentage]
    negative_group = dataframe[dataframe['percentage']<=total_avg_percentage]
    
    column_header_name = positive_group.columns.values[0]
    created_sentence = []
    groups = pd.DataFrame()
    groups = groups.append(positive_group.head(2))
    groups = groups.append(negative_group.tail(3),ignore_index=True)
    for row in groups.iterrows():
        subject = '<span class="bold number">'+ str('{:.2f}'.format(round(row[1]['percentage'],2))) + '%</span>'+ column_header_name + ' ' 
        object = '<span class="bold">'+str(row[1][column_header_name])+'</span>'
        payload = get_sentence_payload(subject, 'be', object)
        created_sentence.append(nlg_service(payload))
        #print(round(row[1]['percentage'],2))

    return created_sentence

def get_splitup_insight(dataframe):
    dataframe['percentage'] = dataframe["Counts"]/dataframe["Counts"].sum() * 100
        
    good_group = dataframe[dataframe['percentage']>70]
    avg_group = dataframe[(dataframe['percentage']> 40) & (dataframe['percentage'] <=70)]
    poor_group = dataframe[(dataframe['percentage']> 0) & (dataframe['percentage'] <=40)]
    return ''

def build_insights(dataframe):
    sentences = []
    sentences.extend(get_average_insight(dataframe))
    sentences.append(get_splitup_insight(dataframe))
    return sentences

def getInsights(dataframe, user_selections):
    
    # user_selection is an OrderedDict, so the order of user choice is maintained. It can be iterated as below:
    context=[]
    insights=[]
    if user_selections is not None:
            for item in user_selections.items():
                sentence='<span class="bold">'+item[0]+'</span> is <span class="bold">'+item[1]+'</span>'
                context.append(sentence)
    
    if len(context) > 0:
        payload = get_context(context)
        context_sentence = nlg_service(payload)
        insights.append('When '+context_sentence[:-1]+',')

    #print("getInsights called with user selection = ", user_selections)
    #print("DataSet")
    #print(dataframe)
    insights.extend(build_insights(dataframe))
    return insights   
    

if __name__ == "__main__":
    '''sentence = get_sentence_payload()
    print("sentence:", sentence)
    sentence_data = json.dumps(sentence, cls=MyEncoder)
    print("sentenceJsonPayload:", sentence_data)

    response = getInsights()
    print("response:", response)'''
    data = pd.read_excel('wMIncidents.xlsx')
    grouped = data["Product Family"].value_counts().reset_index()
    grouped.columns = ["Product Family", "Counts"]
    
    getInsights(grouped, user_selections = None)
    