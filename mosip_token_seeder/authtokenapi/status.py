from datetime import datetime

from .service import AuthTokenService
from .model import BaseHttpResponse


class StatusApi:
    def __init__(self, app, config, logger, authtoken_service : AuthTokenService):
        self.authtoken_service = authtoken_service
        @app.get(config.root.context_path + "authtoken/status/{id}")
        async def fetch_status(id):
            print("id :",id)
            status = authtoken_service.fetch_status(id)
            return BaseHttpResponse(response={
                'status': status
            })
