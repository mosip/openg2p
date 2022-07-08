import json

from datetime import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..model import BaseHttpResponse, BaseError
from . import MOSIPTokenSeederException, MOSIPTokenSeederNoException

class RequestValidationErrorHandler:
    def __init__(self, app, config, logger):
        @app.exception_handler(Exception)
        async def validation_exception_handler(request, exc):
            status_code = 400
            if isinstance(exc, MOSIPTokenSeederNoException):
                code = exc.error_code
                message = exc.error_message
                status_code = exc.return_status_code
            elif isinstance(exc, MOSIPTokenSeederException):
                code = exc.error_code
                message = exc.error_message
            else:
                l = str(exc).split('::')
                if len(l)>1:
                    code = l[0]
                    message = l[1]
                else:
                    code = 'ATS-REQ-100'
                    message = l[0]
            res = BaseHttpResponse(
                errors=[
                    BaseError(
                        errorCode=code,
                        errorMessage=message
                    )
                ],
                response=None
            )
            res_dict = json.loads(res.json())
            return JSONResponse(content=res_dict, status_code=status_code)