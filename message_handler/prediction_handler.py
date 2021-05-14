'''
Created on Apr 29, 2019

@author: moonjaewon
'''
import os
import requests
import numpy as np
from flask import jsonify

def prediction_handler(subpath, data):
    if subpath =='LR_salary':
        import pickle
        # hard coding recent_file

        model_name = subpath
        model_version = data['model_version']
        partial_model = data['partial_model']
        model_format = data['model_format']
        input_v = np.array(data['exp'])
        
        download_folder = os.path.join("model", model_name, partial_model, model_version)
        model_file_name ='model.'+model_format
        model_address = os.path.join(download_folder, model_file_name)
        print(model_address)
        model = pickle.load(open(model_address,'rb'))
        # Get the data from the POST request.
        
        # Make prediction using model loaded from disk as per the data.
        prediction = model.predict([[input_v]])
        # Take the first value of prediction
        output = prediction[0]
        result = jsonify(output)
        
    return result