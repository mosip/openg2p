import uuid

from .. import app, config

from . import model
from . import utils

supported_output_types = ['json','csv']
supported_delivery_types = ['download']

# @app.post(config.root.context_path + "authtoken/json")
# def authtoken_json(requestbody : model.AuthTokenRequestModel):
#     if requestbody is None:
#         return {
#             "message": "no input found"
#         }, 400

#     if requestbody.request is None:
#         return {
#             "message": "request format not found"
#         }, 400

#     if requestbody.request.output is None:
#         return {
#             "message": "output type is not mentioned"
#         }, 400

#     if requestbody.request.output not in supported_output_types:
#         return {
#             "message": "output type not supported"
#         }, 400

#     if requestbody.request.deliverytype is None:
#         return {
#             "message": "delivery type is not mentioned"
#         }, 400

#     if requestbody.request.deliverytype  not in supported_delivery_types:
#         return {
#             "message": "delivery type not supported"
#         }, 400

#     txn_id = str(uuid.uuid4())

#     return {
#         'txnId': txn_id,
#         # 'data': data.dict(),
#         'input': 'json',
#         # 'output': output,
#         # 'deliverytype': deliverytype,
#     }
from . import token_seeder