import array
import datetime
import json


from pydantic import BaseModel
from typing import List, Optional


 # {
    #     "vid": "2014391641351279",
    #     "name": [{"language":"eng", "value": "EMANASAR-TEST-6"}],
    #     "gender": [{"language":"eng", "value": "Male"}],
    #     "dateOfBirth": "1976-01-01",
    #     "phoneNumber": "8360334018",
    #     "emailId": "PRASHANT.SINGH@IIITB.AC.IN",
    #     "fullAddress": [{"language":"eng", "value": "BANGALORE, Electronics City, Bengaluru, Karnataka, 560016"}]
# }


class AuthTokenBaseModel(BaseModel):
    vid: Optional[str]
    name: Optional[str]
    gender: Optional[str]
    dateOfBirth: Optional[str]
    phoneNumber: Optional[str]
    emailId: Optional[str]
    fullAddress: Optional[str]

