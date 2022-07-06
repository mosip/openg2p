from datetime import datetime
import json

from pydantic import BaseModel
from typing import List

class AuthTokenModel(BaseModel):
    output: str
    deliverytype: str
    authdata: List[str]

