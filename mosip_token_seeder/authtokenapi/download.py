from datetime import datetime
from fastapi import Response

from .service import AuthTokenService
from .exception import MOSIPTokenSeederException


class DownloadApi:
    def __init__(self, app, config, logger):
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