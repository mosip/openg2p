import array
import datetime
import json


from pydantic import BaseModel
from typing import List, Optional

class AuthTokenRequestModel(BaseModel):
    auth_request_id: Optional[str]
    input_type: Optional[str]
    output_type: Optional[str]
    delivery_type: Optional[str]
    status: Optional[str]
    created_time: Optional[str]
    updated_time: Optional[str]

