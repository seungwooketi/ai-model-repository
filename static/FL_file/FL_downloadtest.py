'''
Created on Mar 3, 2020

@author: moonjaewon
'''
from FL_util import FL_model 

repository_address ='http://0.0.0.0:8080/'
"""
#Define model information including model name, model version, and model location.
#Set the initial model version to 0.0. 
#The version of each AI model can be described up to one decimal place.
## Model name: The model name to be registered must be unique. Check the name of the registered model (visit:/repository_structure)
## Model version: Models with the same name can have multiple versions. The model version can be described up to the first decimal place.
## Model location (server/client): 
##### server: The server registers an initial AI model and updates an advanced global model using the model created by clients. The updated model is registered again in the repository.
##### client: The client uses the initial model with local data to update the local model. It also uploads the updated parameters to the repository.
## device name: The name of device
"""

model_info={
   "model_name":"DECENTER_UC4_FL", 
   "model_version":"0.0", #0.0(initial) 
   "model_location":"server", #server or client
   "device_name":"ID0002" #registered file name on AI model repository 
   #Download URL: model_download_FL?model_name=DECENTER_UC4_FL&model_version=0.0&model_location=client&device_name=ID0001&
}

# Create instance using FL_repository 
FL = FL_model(repository_address)

# Set an model information attribute
FL.set_model_info(model_info)

"""
# model upload code
# 2. Download the model for server & client
# 2-1. Declare the file name to be used when saving on local storage
# 2-2. Download the model using API
"""

stored_file_name = "../test_model_storage/model_s_.zip"
FL.set_stored_file_name(stored_file_name)
Fl_model=FL.model_download()
FL.model_save(Fl_model)
    
    
    
    