'''
Created on May 2, 2019

@author: moonjaewon
'''

import glob
import json

class ModelInformation(object):
    '''
    classdocs
    '''
    def __init__(self, model_folder):
        '''
        Constructor
        '''
        self.MODEL_FOLDER = model_folder
        self.all_model_information =  self.get_all_model_information()

    
    def get_all_model_information(self):
        model_specification_files=[]
        for model_folder in self.MODEL_FOLDER:
            temp = glob.glob(model_folder)
            model_specification_files = model_specification_files+temp
            print(model_specification_files)
    
        results_all = []
        for specification_file in model_specification_files:
            json_data = open(specification_file).read()
            data = json.loads(json_data)
            temp_all = data
            results_all.append(temp_all)
        
        model_all = json.dumps(results_all, indent=6)
        return model_all
         
    def get_format_count(self):
        from collections import Counter
        model_list = json.loads(self.all_model_information)
        input_type_list = Counter(indi_model['model']['input_type']for indi_model in model_list)

        return input_type_list
        #c = Counter(self.model_all_specification)

if __name__=='__main__':
    MODEL_FOLDER ='../model/*/*/*/info.json'
    
    ms = ModelInformation(MODEL_FOLDER)  
    count_list = ms.get_format_count()
    #print(count_list['image'])




    