from datetime import datetime
from fastapi import Request
import uuid

from mosip_token_seeder.service.seeder_exception import SeederException

from ..service.authtoken_request_service import AuthTokenService

# from ..model.authtokenrequestmodel import AuthTokenRequestModel
from .. import app, settings
from pydantic import BaseModel

supported_output_types = ['json','csv']
supported_delivery_types = ['download']



@app.post(settings.root.context_path + "authtoken/json")
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
        return request_identifier
    except SeederException as exception:
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
                "errorCode": "string",
                "message": "string"
                }
            ],
            "response": None
        } 
        
        {



            "message": str(exception)
        }, 200
    #     pass
        

    txn_id = str(uuid.uuid4())

    return {
        'txnId': txn_id,
        # 'data': data.dict(),
        'input': 'json',
        # 'output': output,
        # 'deliverytype': deliverytype,
    }