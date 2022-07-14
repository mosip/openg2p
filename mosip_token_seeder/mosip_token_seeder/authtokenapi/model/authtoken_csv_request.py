from typing import Literal, Union
from . import AuthTokenHttpRequest, AuthTokenRequest, MapperFields, MapperFieldIndices

class AuthTokenCsvRequestWithHeader(AuthTokenRequest):
    csvWithHeader : Literal[True]
    mapping : MapperFields = MapperFields()
    csvDelimiter : str = ','

class AuthTokenCsvRequestWithoutHeader(AuthTokenRequest):
    csvWithHeader : Literal[False]
    mapping : MapperFieldIndices = MapperFieldIndices()
    csvDelimiter : str = ','

AuthTokenCsvRequest = Union[AuthTokenCsvRequestWithHeader, AuthTokenCsvRequestWithoutHeader]

class AuthTokenCsvHttpRequest(AuthTokenHttpRequest):
    request : AuthTokenCsvRequest
