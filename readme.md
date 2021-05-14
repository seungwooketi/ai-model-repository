# 1. AI model repository

## 1.1 Introduction

We developed this AI model repository to support the DECENTER infrastructure to deploy distributed AI applications. The structure of each application must be a set of microservices and one microservice can use one or more  AI models.
The developer uploads AI model data to let any microservice access this intelligence efficiently. Each microservice can download the proper AI data by REST API.


## 1.2 How to use the AI model repository

We firstly installed this into the private server. Any developer who wants to upload their models or find the proper model can use this repository by visiting http://182.252.132.39:5000/home

## 2. The main menu of AI model repository
### Repository structure ###
```
 You can explore the storage status of the AI model repository
```
### General model manager
```
* Registration
* Information
  - Model meta information
  - Model summary
  - Model description
* How to download
```
### FL model manager
```
 * How to upload
 * How to download
```

## 2.1 General model manager
### 2.1.1 Registration

When you register an AI model, you can easily upload the AI ​​model through the registration menu. It requires model name, model version, model format, input type, and model split information. In addition, it also needs optional information such as purpose, target, preferred computation method, and tag. The registration form is automatically generated based on the pre-defined model information schema.


### 2.2.2  information

- Model meta-information: You can explore the information on all registered models. This information is automatically created after registration.
- Model summary: This menu shows the summary table of all registered models.
- Model description: This menu shows the schema and one example of the model description.

### 2.2.3 How to download
This page shows how to download the proper model. Each micro-service can use this API to download the model easily from the Model Repository. This server provides multiple AI models which can classify, predict the future status. This repository server provides simple API to access and download the right model for a local edge. This REST API have four types of parameters: model_name, model_version, model_split, and split_number.

```
 - example:http://182.252.132.39:5000/model_download?model_name=UC4_FaceDetection&model_version=0.1&model_split=Split_No&split_number=0
```
## 2.2 FL model manager

The role of the data repository in the Federated Learning system is to register and deliver the model by both server and client sides. We developed this AI data repository to support the Federataed Learning in DECENTER . 

### 2.2.1 How to upload

When the server requests registration of a new global model, the repository finds suitable storage space for the task. When there is adequate storage space based on the model name (task name), AI model data is stored along with the version information. This repository also update the model data with the existing version. A server with appropriate capabilities can register its own generated global model data and participate in Federated Leearning at any time. 

The clients can import the global model and update/register the local model. The version of the global model is checked first, then the client model is stored on the corresponding storage.

### 2.2.2 How to download

First, the client needs to import the appopriate global model data in order to generate local model data for Federated learning. THe repository finds the proper version of the global model and passes it to the client. The server also needs client data to update the global model. The server collects updated client data based on a specific version of global data and does aggregation.


### 2.2.3 Basic parameters

The four parameter values are the basic requirements for uploading or downloading the model to the management system: Task_Name, Version, Model_Location, and Device_Name

```
 * Task_Name: a parameter to present the identity of each task to be solved using Federated Learning. Any server and client that has the ability to perform the specific task can be a candidate for participation. The data management system may inform the conditions of the device to perform each task. 
 
 * Version: a float value used when the server updates global AI model data. When multiple servers and clients work together in one task, this version is the basis for managing the output
 
 * Model_Location: information about the device where AI data was first created. There are global models created on the serve and local models created on the client. The server requests the local model, and the client request the global model. 
 
 * Device_Name: a unique ID or name of each device.
```

