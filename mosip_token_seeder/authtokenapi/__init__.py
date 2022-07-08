from .exception import RequestValidationErrorHandler
from .authtoken import AuthTokenApi
from .ping import PingApi
from .status import StatusApi
from .download import DownloadApi


def initialize(app, config, logger, request_id_queue):
    api_exception_handler = RequestValidationErrorHandler(app, config, logger)
    auth_token_api = AuthTokenApi(app,config,logger, request_id_queue)
    ping_api = PingApi(app, config, logger)
    status_api = StatusApi(app, config, logger, auth_token_api.authtoken_service)
    download_api = DownloadApi(app, config, logger, auth_token_api.authtoken_service)
    return (
        api_exception_handler,
        auth_token_api,
        ping_api,
        status_api,
        download_api
    )
