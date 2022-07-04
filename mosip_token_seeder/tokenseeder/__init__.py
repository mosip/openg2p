import uuid
from . import app, settings
from pydantic import BaseModel

supported_output_types = ['json']
supported_delivery_types = ['sync']

class TokenSeederRequest(BaseModel):
    name : str


@app.post(settings.root.context_path + 'authtoken/json')
def authtoken_json(data : TokenSeederRequest, output : str = 'json', deliverytype : str = 'sync'):
    if output not in supported_output_types:
        return {
            'message': 'output type not supported'
        }, 400
    if deliverytype not in supported_delivery_types:
        return {
            'message': 'delivery type not supported'
        }, 400

    txn_id = str(uuid.uuid4())

    return {
        'txnId': txn_id,
        'data': data.dict(),
        'input': 'json',
        'output': output,
        'deliverytype': deliverytype,
    }