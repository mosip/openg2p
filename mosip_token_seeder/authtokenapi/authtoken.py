from datetime import datetime
from fastapi import Request

from mosip_token_seeder.repository import db_tools

from .service import AuthTokenService
from .exception import MOSIPTokenSeederException
from .model import AuthTokenHttpRequest, BaseHttpResponse

class AuthTokenApi:
    def __init__(self, app, config, logger, request_id_queue):
        self.authtoken_service = AuthTokenService(config, logger, request_id_queue)

        @app.post(config.root.context_path + "authtoken/json")
        async def authtoken_json(request : AuthTokenHttpRequest):
            ##call service to save the details.
            request_identifier = self.authtoken_service.save_authtoken_json((request.request))
            return BaseHttpResponse(response={
                'request_identifier': request_identifier
            })
