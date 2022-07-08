from datetime import datetime

from .service import AuthTokenService
from .exception import MOSIPTokenSeederException


class StatusApi:
    def __init__(self, app, config, logger):
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
                    'responsetime': datetime.utcnow(),
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
                    'responsetime': datetime.utcnow(),
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
