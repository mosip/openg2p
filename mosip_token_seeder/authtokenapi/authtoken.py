from datetime import datetime
import logging
import re
import traceback
from fastapi import Request, Response
import uuid



from mosip_token_seeder.authtokenapi.service.authtoken_request_service import AuthTokenService
from mosip_token_seeder.authtokenapi.service.mosip_token_seeder_exception import MOSIPTokenSeederException
from fastapi.responses import StreamingResponse
# from ..model.authtokenrequestmodel import AuthTokenRequestModel
from .. import app, config

supported_output_types = ['json','csv']
supported_delivery_types = ['download']
logger = logging.getLogger(__name__)

@app.post(config.root.context_path + "authtoken/json")
async def authtoken_json(request : Request):
    try:
        requestjson = await request.json()
    except Exception as exception:
        logger.exception(exception)        
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
    
    authtokenjson = requestjson["request"]
    
    
    if authtokenjson is None:
        logger.error("auth request format not found")        
        return {
            "message": "auth request format not found"
        }, 400

    if authtokenjson["output"] is None:
        logger.error("output type is not mentioned")
        return {
            "message": "output type is not mentioned"
        }, 400

    if authtokenjson["output"] not in supported_output_types:
        logger.error("output type not supported")
        return {
            "message": "output type not supported"
        }, 400

    if authtokenjson["deliverytype"] is None:
        logger.error("delivery type is not mentioned")
        return {
            "message": "delivery type is not mentioned"
        }, 400

    if authtokenjson["deliverytype"]  not in supported_delivery_types:
        logger.error("delivery type not supported")
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
        logger.exception(exception)
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
        logger.exception(exception)
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
async def fetch_status(id):
    print("id :",id)
    authtoken_service = AuthTokenService()
    try:
        status = authtoken_service.fetch_status(id)
        return {
            'id': '',
            'version': '0.1',
            'metadata': {},
            'responsetime': datetime.now(),
            'errors': None,
            'response': {
                'status': status
            }
        }  
    except MOSIPTokenSeederException as exception:
        logger.exception(exception)
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
        logger.exception(exception)
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

@app.get(config.root.context_path + "authtoken/file/{id}")
async def download_file(id):
    print("id :",id)
    authtoken_service = AuthTokenService()

    try:
        output_bytes = authtoken_service.get_file(id)
        return Response(content=output_bytes, media_type="text/plain")
    except MOSIPTokenSeederException as exception:
        #pass on proper response object 
        logger.exception(exception)
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

