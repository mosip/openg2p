from urllib.request import Request
import uuid

from model.authtokenrequestmodel import AuthTokenRequestModel
from .. import app, settings
from pydantic import BaseModel

supported_output_types = ['json','csv']
supported_delivery_types = ['download']



@app.post(settings.root.context_path + "authtoken/json")
def authtoken_json(requestbody : AuthTokenRequestModel):
    if requestbody is None:
        return {
            "message": "no input found"
        }, 400

    if requestbody.request is None:
        return {
            "message": "request format not found"
        }, 400

    if requestbody.request.output is None:
        return {
            "message": "output type is not mentioned"
        }, 400

    if requestbody.request.output not in supported_output_types:
        return {
            "message": "output type not supported"
        }, 400

    if requestbody.request.deliverytype is None:
        return {
            "message": "delivery type is not mentioned"
        }, 400

    if requestbody.request.deliverytype  not in supported_delivery_types:
        return {
            "message": "delivery type not supported"
        }, 400

    txn_id = str(uuid.uuid4())

    return {
        'txnId': txn_id,
        # 'data': data.dict(),
        'input': 'json',
        # 'output': output,
        # 'deliverytype': deliverytype,
    }