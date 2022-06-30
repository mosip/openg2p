from importlib.metadata import metadata
from pydantic import BaseModel
from typing import List

class MOSIPRequestedAuth(BaseModel):
    demo : bool = False
    pin : bool = False
    otp : bool = False
    bio : bool = False

class MOSIPEncryptAuthRequest(BaseModel):
    timestamp : str
    demographics : dict
    biometrics : list

class MOSIPAuthRequest(BaseModel):
    id : str
    version : str
    individualId: str
    transactionID: str
    requestTime: str
    specVersion: str
    thumbprint: str
    domainUri: str
    env: str
    requestedAuth : MOSIPRequestedAuth = MOSIPRequestedAuth()
    consentObtained: bool
    requestHMAC: str
    requestSessionKey: str
    request: str
    metadata: dict
