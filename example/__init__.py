import logging
import json
import time
import pyodbc
import datetime

import azure.functions as func
from configparser import ConfigParser

def default(o):
    if isinstance(o,(datetime.datetime, datetime.date)):
        return o.isoformat()



#Initial script file must have main
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #read in params
    # table_name=req.params.get('table_name','DT_idx_XBRL')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
