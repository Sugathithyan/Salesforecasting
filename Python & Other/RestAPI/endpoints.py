import logging
from RestAPI.arima import arima_model
from flask_pymongo import pymongo
from flask import jsonify, request
import pandas as pd


con_string = "mongodb+srv://Sugathithyan_M:sugAthithyAn@mycluster.czhpfbp.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_string)
db = client.get_database('users')
user_collection = pymongo.collection.Collection(db, 'fir_db')
print("MongoDB connected Successfully")

pmts={}

def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Read Operation'
        print("Read Operation")
        return res

    @endpoints.route('/register_user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


   

    @endpoints.route('/read-users',methods=['GET'])
    def read_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
            }
            output = [{'email' : user['email'], 'pass' : user['pass']} for user in users]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/update-users',methods=['PUT'])
    def update_users():
        resp = {}
        try:
            req_body = request.json
            user_collection.update_one({"name":req_body['name']}, {"$set": req_body['updated_user_body']})
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    



    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            df = pd.read_csv(file)
            global pmts
            pmts=arima_model(df)
            status = {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

        
    @endpoints.route('/get_data',methods=['GET'])
    def get_data():
        return pmts

    return endpoints
