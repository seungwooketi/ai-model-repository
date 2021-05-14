'''
Created on Apr 23, 2019

@author: moonjaewon
'''
from flask import Flask, request, send_from_directory, render_template, send_file, json, jsonify, url_for
from flask_bootstrap import Bootstrap
from flask import copy_current_request_context
import requests, shutil

import os
from flask_autoindex import AutoIndex 
import pathlib
from werkzeug.utils import cached_property
#werkzeug.cached_property = werkzeug.utils.cached_property

import config as myConfig 
from message_handler import prediction_handler as ph
from message_handler import Model_Information as mi


# set the project root directory as the static folder, you can set others.
STATIC_URL_PATH ='/static'
STATIC_FOLDER='static'
INFO_FILE_NAME = 'info.json'

app = Flask(__name__, static_url_path=STATIC_URL_PATH, static_folder=STATIC_FOLDER)

app.config['MAX_CONTENT_LENGTH'] = 1024*1024 * 1024 * 1024

Bootstrap(app)
root_dir = os.path.join(os.path.curdir,'model')
AutoIndex(app, browse_root=root_dir)

# Clearly change
model_name=None
MODEL_FOLDER ={'model/*/*/*/*/'+INFO_FILE_NAME}


@app.route('/home')
def home():
    modelInfo =  mi.ModelInformation(MODEL_FOLDER)
    print(modelInfo)
    input_type_count_list = dict(modelInfo.get_format_count())
    print(input_type_count_list)
    return render_template('home.html', model_count = input_type_count_list)


@app.route('/model_information_registration')   # URL '/' to be handled by main() route handler
def main():
    return render_template('model_information_registration.html')


@app.route('/model_upload', methods=['POST','GET'])
def model_upload(): 
    print('upload') 
    model_folder = request.args['model_path']
    return render_template("model_upload_form.html", data = model_folder)  

@app.route('/model_upload_success', methods = ['POST','GET'])  
def success():  
    if request.method == 'POST':  
        folder = request.form.get('folder')  
        f = request.files['file']  
        #f.filename
        filename ='model.zip'
        f.save(os.path.join(folder, filename))
        #f.save(f.filename)  
        return render_template("model_upload_success.html", file_name = filename, file_folder = folder)  
    
@app.route('/Dir_make_General', methods=['POST','GET'])
def makeDir_infofile():
    model = request.get_json(silent=True)
    model_spec = model['model']
    model_name = model_spec['model_name']
    model_version = model_spec['model_version']
    model_split = model_spec['model_split']
    split_number = model_spec['split_number']
    model_path = os.path.join("model", model_name, model_split,'v'+str(model_version), 's'+str(split_number))
    os.makedirs(model_path, exist_ok=True)
    
    info_json_path = os.path.join(model_path, INFO_FILE_NAME)
    with open(info_json_path, 'w') as f:
        json.dump(model, f) 
    return model_path

ALLOWED_EXTENTIONS = {'zip', 'txt', 'pdf'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS

def saveModelByPost(request, folder):
    if request.method =='POST':
        if 'file' not in request.files:
            print('No File')
        else:
            file = request.files['file'] 
            if file.filename =='':
                print('No Selected File')
            if file and allowed_file(file.filename):
                filename = file.filename
                print('start_saving')
                file.save(os.path.join(folder, file.filename))
                print('end_saving')

        
@app.route('/Model_upload_FL', methods = ['GET','POST'])
def FL_model_save():
    folder = request.args.get('folder') 
    print(folder)
    saveModelByPost(request, folder)
    
    return folder
    

def FL_dir_make(model_info):   
    model_name = model_info['model_name']
    model_version = model_info['model_version']
    model_location = model_info['model_location']
    model_path = os.path.join("model",'FL', model_name, 'v'+str(model_version), model_location)
    os.makedirs(model_path, exist_ok=True)
    return model_path
    
@app.route('/FL_upload_path_make', methods = ['POST'])      
def FL_model_upload():
    model_info = request.get_json(force=True)
    #model_info = data['model_info']
    model_path = FL_dir_make(model_info)

    return model_path

@app.route('/model_download_FL',  methods=["GET", "POST"])
def model_download_FL():                                                                                                                                                                
    #http://182.252.132.39:5000/model_download_FL?model_name=decenter_mnist&model_version=0.1&model_location=server&device_name=keti&
    model_name = request.args.get('model_name')
    model_version = 'v'+ request.args.get('model_version')
    model_location = request.args.get('model_location')
    model_file_name = request.args.get('device_name')+'_data.zip'
    
    download_folder = os.path.join("model","FL", model_name, model_version, model_location)

    print(download_folder, model_file_name)
    return send_from_directory(directory=download_folder, filename= model_file_name, as_attachment=True)

@app.route('/model_download',  methods=["GET", "POST"])
def model_download_general():
     
    #http://0.0.0.0:8080/model_download?model_name=VGG16&model_split=Split_No&model_version=v0.1&split_number=s0
    model_name = request.args.get('model_name')
    model_split = request.args.get('model_split')
    model_version = 'v'+request.args.get('model_version')
    split_number = 's'+request.args.get('split_number')
    print(model_name, model_split, model_version, split_number)
    download_folder = os.path.join("model", model_name, model_split, model_version, split_number)
    model_file_name ='model.zip'

    print(download_folder, model_file_name)
    return send_from_directory(directory=download_folder, filename= model_file_name, as_attachment=True)
#
# How_to
@app.route('/howto_download_general', methods=["GET", "POST"])
def howto_download_general():
    return render_template('howto_download_general.html')

@app.route('/howto_upload_FL', methods=["GET", "POST"])
def howto_upload_FL():
    return render_template('howto_upload_FL.html')

@app.route('/howto_download_FL', methods=["GET", "POST"])
def howto_download_FL():
    return render_template('howto_download_FL.html')
####

@app.route('/model_description', methods=["GET", "POST"])
def model_description():
    modelInfo =  mi.ModelInformation(MODEL_FOLDER)
    json_example_ = json.loads(modelInfo.all_model_information)
    json_example_ = json_example_[0]
    json_schema_file = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'static','schema','model_data_v2.json')
    json_schema_= json.load(open(json_schema_file))
    return render_template('model_description.html', json_example =json_example_, json_schema = json_schema_)    

@app.route('/schema_description', methods=["GET", "POST"])
def schema_description():
    return render_template('schema_description.html')
    
@app.route('/repository_structure', methods=["GET", "POST"])
def repository_structure():
    return render_template('repository_structure.html')

@app.route('/api/<path:subpath>',methods=['POST'])
def predict(subpath):
    data = request.get_json(force=True)    
    result = ph.prediction_handler(subpath, data) 
    return result

@app.route('/all_model_specification', methods=["GET", "POST"])
def model_specification():
    modelInfo =  mi.ModelInformation(MODEL_FOLDER)
    return render_template('registered_model_list_view.html', json_model_all = modelInfo.all_model_information)

@app.route('/model_detail', methods=["GET", "POST"])
def model_detail():
    modelInfo =  mi.ModelInformation(MODEL_FOLDER)
    return render_template('json_detail.html', json_model_all = modelInfo.all_model_information)

@app.route('/model_register', methods=["GET", "POST"])
def model_register():
    return render_template('model_register.html')


if __name__ == '__main__':
 #   uploads = os.path.join("/model", "download")
    app.run(host=myConfig.BASE_URL, debug=myConfig.DEBUG, port = myConfig.PORT, threaded=True)
    application = app
