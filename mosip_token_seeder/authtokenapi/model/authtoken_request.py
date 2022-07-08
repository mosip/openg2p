from pydantic import BaseModel, validator
from typing import List, Optional

from ..exception import MOSIPTokenSeederException

supported_output_types = ['json','csv']
supported_delivery_types = ['download']

class AuthTokenRequest(BaseModel):
    output: str
    deliverytype: str
    authdata: Optional[List[dict]]
    mapping: Optional[dict]
    lang: Optional[str]

    @validator('output', pre=True)
    def output_valid(cls, value):
        if not value:
            raise MOSIPTokenSeederException('ATS-REQ-100','output type is not mentioned')
        if value not in supported_output_types:
            raise MOSIPTokenSeederException('ATS-REQ-100','output type is not supported')
        return value
    
    @validator('deliverytype', pre=True)
    def delivery_valid(cls, value):
        if not value:
            raise MOSIPTokenSeederException('ATS-REQ-100','delivery type is not mentioned')
        if value not in supported_delivery_types:
            raise MOSIPTokenSeederException('ATS-REQ-100','delivery type is not supported')
        return value
    
    @validator('authdata')
    def auth_data_validate(cls, value):
        if not value:
            raise MOSIPTokenSeederException('ATS-REQ-001','authdata missing')
        return value
