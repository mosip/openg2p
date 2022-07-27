from pydantic import BaseModel, validator
from typing import List, Optional

from . import AuthTokenHttpRequest

from . import AuthTokenBaseRequest

from ..exception import MOSIPTokenSeederException
from . import MapperFields

supported_output_types = ['json','csv']
supported_delivery_types = ['download']


class ODKConfig(BaseModel):
    print("ODKConfig called")
    odataurl : str = "odataurl"
    baseurl : str = "baseurl"
    version : str = "version"
    projectid : str = "projectid"
    formid : str = "formid"
    emailId : str = "emailId"
    password : str = "password"
    startdate : str = "startdate"
    enddate : str = "enddate"


class AuthTokenODKRequest(AuthTokenBaseRequest):
    print("AuthTokenODKRequest called")
    odkconfig : ODKConfig

    # @validator('odkconfig')
    # def auth_data_validate(cls, value):
    #     if not value:
    #         raise MOSIPTokenSeederException('ATS-REQ-102','authdata missing')
    #     return value
    # pass

class AuthTokenODKHttpRequest(AuthTokenHttpRequest):
    print("AuthTokenODKHttpRequest called")
    request : AuthTokenODKRequest
    