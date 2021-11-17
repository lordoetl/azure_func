import logging
import json
import time
import joblib

import pandas as pd



import datetime

import azure.functions as func
from configparser import ConfigParser

def default(o):
    if isinstance(o,(datetime.datetime, datetime.date)):
        return o.isoformat()

lr = joblib.load("model.pkl") # Load "model.pkl"
print ('Model loaded')
model_columns = joblib.load("model_columns.pkl") # Load "model_columns.pkl"
print ('Model columns loaded')


#Initial script file must have main
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #read in params
    # table_name=req.params.get('table_name','DT_idx_XBRL')
    age = req.params.get('age')
    sex=req.params.get('sex')
    embarked=req.params.get('embarked')
    print(age)
    print(sex)
    print(embarked)
   
    json_=pd.DataFrame([[age,sex,embarked]],columns=['age','sex','embarked'])



    # json_=pd.DataFrame(data=d)
    # json_ = request.json
    print(json_)
    query = pd.get_dummies(pd.DataFrame(json_))
    query = query.reindex(columns=model_columns, fill_value=0)

    prediction = list(lr.predict(query))
    print(prediction)
    # return jsonify({'prediction': str(prediction)})
    if not age:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            age = req_body.get('Age')
    
    
    print(prediction[0])

    if age:
        # return func.HttpResponse({'prediction': str(prediction)})
        # return 'stuff'
        return func.HttpResponse(f"Hello, if you were a {age} year old {sex}  and got on at {embarked}, You would have likely {'survived' if prediction[0]==1 else 'died' }")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
