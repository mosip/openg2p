import datetime
import json

from pydantic import BaseModel
from typing import List

from model.authtokenmodel import AuthTokenModel

class AuthTokenRequestModel(BaseModel):
    id: str
    version: str
    metadata: str
    requesttime: datetime
    request: AuthTokenModel

