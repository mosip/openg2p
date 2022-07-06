 # CREATE TABLE "auth_request_data" (
        #     "auth_request_id"	TEXT NOT NULL,
        #     "auth_request_line_no"	INTEGER NOT NULL,
        #     "auth_data"	TEXT NOT NULL,
        #     "auth_data_return"	TEXT,
        #     "token"	TEXT,
        #     "status"	TEXT NOT NULL,
        #     "created_time"	TEXT NOT NULL,
        #     "updated_time"	TEXT,
        #     PRIMARY KEY("auth_request_line_no")
        # )
        # """)


from typing import Optional
from pydantic import BaseModel


class AuthTokenRequestDataModel(BaseModel):
    auth_request_id: Optional[str]
    auth_request_line_no: Optional[int]
    auth_data_recieved: Optional[str]
    auth_data_output: Optional[str]
    auth_data_input: Optional[str]
    token: Optional[str]
    status: Optional[str]
    created_time: Optional[str]
    updated_time: Optional[str]