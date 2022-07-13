from datetime import datetime

from .service import AuthTokenService
from .model import BaseHttpResponse


class StatusApi:
    def __init__(self, app, config, logger, authtoken_service : AuthTokenService):
        self.authtoken_service = authtoken_service
        self.logger = logger
        @app.get(config.root.context_path + "authtoken/status/{id}")
        async def fetch_status(id):
            # self.logger.info("Status api called. Req id :",id)
            status = self.authtoken_service.fetch_status(id)
            return BaseHttpResponse(response={
                'status': status
            })
