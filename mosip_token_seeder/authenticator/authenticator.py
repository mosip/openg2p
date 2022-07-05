import string
import secrets
from datetime import datetime
from . import model
from .utils import RestUtility, CryptoUtility

class MOSIPAuthenticator:
    def __init__(
        self,
        auth_rest_util : RestUtility,
        encrypt_cryptoutil : CryptoUtility,
        sign_cryptoutil : CryptoUtility,
        ida_auth_domain_uri,
        partner_misp_lk,
        partner_id,
        partner_apikey,
        ida_auth_version,
        ida_auth_request_id,
        ida_auth_env,
        authorization_header_constant,
        timestamp_format,
        **kwargs
    ):
        self.auth_rest_util = auth_rest_util
        self.encrypt_cryptoutil = encrypt_cryptoutil
        self.sign_cryptoutil = sign_cryptoutil

        self.auth_domain_scheme = ida_auth_domain_uri
        
        if not self.auth_rest_util.url.endswith('/'):
            self.auth_rest_util.url += '/'
        self.auth_rest_util.url += partner_misp_lk + '/' + partner_id + '/' + partner_apikey
        
        self.ida_auth_version = ida_auth_version
        self.ida_auth_request_id = ida_auth_request_id
        self.ida_auth_env = ida_auth_env
        self.timestamp_format = timestamp_format
        self.authorization_header_constant = authorization_header_constant

        self.auth_request = model.MOSIPAuthRequest(
            id=self.ida_auth_request_id,
            version=self.ida_auth_version,
            env=self.ida_auth_env,
            domainUri=self.auth_domain_scheme,
            specVersion=self.ida_auth_version,
            consentObtained=True,
            metadata={},
            thumbprint=self.encrypt_cryptoutil.thumbprint,
            individualId='',
            transactionID='',
            requestTime='',
            request='',
            requestSessionKey='',
            requestHMAC='',
        )
    
    def perform_demo_auth(self, data : dict):
        vid = data.pop('vid')
        demographicData = model.DemographicsModel(**data)
        timestamp = datetime.utcnow()
        timestamp_str = timestamp.strftime(self.timestamp_format) + timestamp.strftime('.%f')[0:4] + 'Z'
        self.auth_request.requestTime = timestamp_str
        self.auth_request.transactionID = ''.join([secrets.choice(string.digits) for _ in range(10)])
        self.auth_request.individualId = vid

        self.auth_request.requestedAuth.demo = True
        
        request = model.MOSIPEncryptAuthRequest(
            timestamp=timestamp_str,
            biometrics=[],
            demographics=demographicData
        )
        
        self.auth_request.request, self.auth_request.requestSessionKey, self.auth_request.requestHMAC = self.encrypt_cryptoutil.encrypt(request.json())

        full_request_json = self.auth_request.json()

        auth_headers = {
            'Authorization': self.authorization_header_constant,
            'content-type': 'application/json',
        }
        auth_headers['Signature'] = self.sign_cryptoutil.json_sign(full_request_json)

        response = self.auth_rest_util.post(data=full_request_json,headers=auth_headers)
        return response.json()
