from datetime import datetime
import re
import traceback
from fastapi import Request
import uuid



from mosip_token_seeder.authtokenapi.service.authtoken_request_service import AuthTokenService
from mosip_token_seeder.authtokenapi.service.mosip_token_seeder_exception import MOSIPTokenSeederException

# from ..model.authtokenrequestmodel import AuthTokenRequestModel
from .. import app, config

supported_output_types = ['json','csv']
supported_delivery_types = ['download']

@app.post(config.root.context_path + "authtoken/json")
async def authtoken_json(request : Request):
    requestjson = await request.json()
    if requestjson is None:
        return {
            "message": "no input found"
        }, 400

    authtokenjson = requestjson["request"]
    if authtokenjson is None:
        return {
            "message": "request format not found"
        }, 400

    if authtokenjson["output"] is None:
        return {
            "message": "output type is not mentioned"
        }, 400

    if authtokenjson["output"] not in supported_output_types:
        return {
            "message": "output type not supported"
        }, 400

    if authtokenjson["deliverytype"] is None:
        return {
            "message": "delivery type is not mentioned"
        }, 400

    if authtokenjson["deliverytype"]  not in supported_delivery_types:
        return {
            "message": "delivery type not supported"
        }, 400

    ##call service to save the details.
    
    authtoken_service = AuthTokenService()

    try:
        request_identifier = authtoken_service.save_authtoken_json((requestjson["request"]))
        return {
            'id': '',
            'version': '0.1',
            'metadata': {},
            'responsetime': datetime.now(),
            'errors': None,
            'response': {
                'request_identifier': request_identifier
            }
        }  
        request_identifier
    except MOSIPTokenSeederException as exception:
        #pass on proper response object 
        return {
            'id': '',
            'version': '0.1',
            'metadata': {},
            'responsetime': datetime.now(),
            'errors': [
                {
                'errorCode': exception.error_code,
                'message': exception.error_message
                }
            ],
            'response': None
        } 
    except Exception as exception:
          
        #pass on proper response object 
        return {
            "id": "string",
            "version": "string",
            "metadata": {},
            "responsetime": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
            "errors": [
                {
                "errorCode": 'ATS-REQ-100',
                "message": str(exception)
                }
            ],
            "response": None
        } 
    
@app.get(config.root.context_path + "authtoken/status/{id}")
async def authtoken_json(id):
    print("id :",id)
    authtoken_service = AuthTokenService()
    status = authtoken_service.fetch_status(id)

