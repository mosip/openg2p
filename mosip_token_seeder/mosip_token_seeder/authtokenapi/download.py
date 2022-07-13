import os
from fastapi.responses import FileResponse

from .service import AuthTokenService


class DownloadApi:
    def __init__(self, app, config, logger, authtoken_service: AuthTokenService):
        self.authtoken_service = authtoken_service
        self.logger = logger
        @app.get(config.root.api_path_prefix + "authtoken/file/{id}")
        async def download_file(id : str):
            # self.logger.info("File api called. Req id :", id)
            self.authtoken_service.assert_download_status(id)
            return FileResponse(os.path.join(config.root.output_stored_files_path, id))