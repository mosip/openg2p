from .exception import RequestValidationErrorHandler
from .authtoken import AuthTokenApi
from .ping import PingApi
from .status import StatusApi
from .download import DownloadApi


def initialize(app, config, logger, request_id_queue):
    api_exception_handler = RequestValidationErrorHandler(app, config, logger)
    auth_token_api = AuthTokenApi(app,config,logger, request_id_queue)
    ping_api = PingApi(app, config, logger)
    status_api = StatusApi(app, config, logger)
    download_api = DownloadApi(app, config, logger)
