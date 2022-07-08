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

authtoken_service = AuthTokenService()


@app.post(config.root.context_path + "authtoken/json")
async def authtoken_json(request : Request):

    requestjson = {}
    
    try:
        requestjson = await request.json()
    except Exception as exception:
        logger.exception(exception)        
        return construct_error_message('ATS-REQ-102', str(exception), '')
       
    authtokenjson = requestjson["request"]
    
    
    if authtokenjson is None:
        logger.error("auth request format not found")        
        return construct_error_message('ATS-REQ-103', 'request object nout found in the input', '')


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
        return construct_error_message(exception.error_code,exception.error_message, '')
        
    except Exception as exception:
        logger.exception(exception)
        return construct_error_message('ATS-REQ-100', str(exception), '')
           
@app.get(config.root.context_path + "authtoken/status/{id}")
async def fetch_status(id):
    
    if id is None :
        logger.exception('ATS-STA-001', 'no input provided')
        return construct_error_message('ATS-STA-001', 'no input provided', '')

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
        return construct_error_message(exception.error_code,exception.error_message, '')

    except Exception as exception:
        logger.exception(exception)
        return construct_error_message('ATS-STA-100', str(exception), '')
        
@app.get(config.root.context_path + "authtoken/download/{id}")
async def download_file(id):
    if id is None :
        logger.exception('ATS-DWN-001', 'no input provided')
        return construct_error_message('ATS-DWN-001', 'no input provided', '')

    try:
        output_bytes = authtoken_service.get_file(id)
        return Response(content=output_bytes, media_type="text/plain")

    except MOSIPTokenSeederException as exception:
        #pass on proper response object 
        logger.exception(exception)
        return construct_error_message(exception.error_code,exception.error_message, '')
       
    except Exception as exception:
        logger.exception(exception)
        #pass on proper response object 
        return construct_error_message('ATS-REQ-100',str(exception), '')

def construct_error_message(eror_code, error_message, id ):
     return {
            'id': id,
            "version": 0.1,
            "metadata": {},
            "responsetime": datetime.now(),
            "errors": [
                {
                "errorCode": eror_code,
                "message": error_message
                }
            ],
            "response": None
        } 