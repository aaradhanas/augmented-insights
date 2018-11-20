from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from shutil import copy
import os

import main
import requests

app = Flask(__name__)
CORS(app)

STATIC_FOLDER = '/static'
ZEMENTIS_URL = 'http://vmisperftest.eur.ad.sag:9083/adapars/model'

@app.route('/getChartInsights/<level>', methods = ['GET'])
def getChartInsights(level):
    if level == '1':
        fileNames = request.args.get('fileNames')
        data = main.getChartsAndInsights(fileNames)
        return jsonify(data)
    else:
        #print('Level = ', level)
        column = request.args.get('column')
        value = request.args.get('value')
        #print('column = ', column , ', value = ', value)
        data = main.getCharts(column, value, level)
        return jsonify(data)

@app.route('/getCharts', methods = ['GET'])
def getCharts():
    columnName = request.args.get('columnName')
    data = main.getCharts(columnName)
    return jsonify(data)

# Upload a file and save it under folder 'static'
@app.route('/uploadFile', methods = ['POST'])
def uploadFile():
    #print('uploadFile')
    if 'file' not in request.files:
        print('No file present')
        return jsonify('FAILED')
    else:
        file = request.files['file']

        if not os.path.exists('./'+ STATIC_FOLDER):
            os.makedirs('./'+ STATIC_FOLDER)
            
        file.save('./'+ STATIC_FOLDER +'/'+file.filename)
        print('File saved successfully')
        return jsonify('SUCCESS')

@app.route('/files', methods = ['GET'])
def listFiles():
    #print('listFiles')
    return jsonify(os.listdir('./'+STATIC_FOLDER))

@app.route('/publishData', methods = ['POST'])
def uploadIntegrationFile():
    print('publishData')
    copy('../data/integration/API-Portal_Analytics.csv', './'+STATIC_FOLDER)
    return jsonify('SUCCESS')

@app.route('/deployToZementis', methods = ['POST'])
def deployToZementis():
    print('deployToZementis')
    #main.generate_pmml_and_deploy()
    with open('./models/PredictiveModel.pmml', 'rb') as f:
        res = requests.post(ZEMENTIS_URL, files= {'file': f}, headers= {'Authorization': 'Basic QWRtaW5pc3RyYXRvcjptYW5hZ2U='})
    print('Response = ', res)
    return jsonify('Model deployed successfully')

if __name__ == "__main__":
    app.run()