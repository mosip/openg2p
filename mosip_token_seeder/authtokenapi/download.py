import os
from fastapi.responses import FileResponse

from .service import AuthTokenService


class DownloadApi:
    def __init__(self, app, config, logger, authtoken_service: AuthTokenService):
        self.authtoken_service = authtoken_service
        @app.get(config.root.context_path + "authtoken/file/{id}")
        async def download_file(id : str):
            print("id :", id)
            self.authtoken_service.assert_download_status(id)
            return FileResponse(os.path.join(config.root.output_stored_files_path, id))