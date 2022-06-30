import os
import json
import secrets
from datetime import datetime
from . import utils
from . import model

class MOSIPAuthenticator:
    def __init__(
        self,
        auth_rest_util,
        auth_domain_scheme,
        encrypt_cryptoutil,
        sign_cryptoutil,
        misp_license_key,
        partner_id,
        api_key,
        oidc_rest_util,
        ida_auth_version,
        ida_auth_request_id,
        ida_auth_env,
        timestamp_format,
    ):
        self.auth_rest_util = auth_rest_util
        self.auth_domain_scheme = auth_domain_scheme
        self.encrypt_cryptoutil = encrypt_cryptoutil
        self.sign_cryptoutil = sign_cryptoutil
        if not self.auth_rest_util.url.endswith('/'):
            self.auth_rest_util.url += '/'
        self.auth_rest_util.url += misp_license_key + '/' + partner_id + '/' + api_key
        self.oidc_rest_util = oidc_rest_util
        self.ida_auth_version = ida_auth_version
        self.ida_auth_request_id = ida_auth_request_id
        self.ida_auth_env = ida_auth_env
        self.timestamp_format = timestamp_format

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
        timestamp = datetime.utcnow()
        timestamp_str = timestamp.strftime(self.timestamp_format) + timestamp.strftime('.%f')[0:3] + timestamp.strftime('%z')
        langCode = data.get('lang','eng')
        mapping = data.get('mapping',{})
        self.auth_request.requestTime = timestamp_str
        self.auth_request.transactionID = secrets.token_hex(10)
        self.auth_request.individualId = data[mapping.pop('vid')['from']]
        
        # hardcoding for now
        request = model.MOSIPEncryptAuthRequest(
            timestamp=timestamp_str,
            biometrics=[],
            demographics={}
        )
        for key in mapping:
            if mapping[key]['withLangCode']:
                request.demographics[key] = [{'language': langCode, 'value': data[mapping[key]['from']]}]
            else:
                request.demographics[key] = data[mapping[key]['from']]
        self.auth_request.request, self.auth_request.requestSessionKey, self.auth_request.requestHMAC = self.encrypt_cryptoutil.encrypt(request.json())

        full_request_json = self.auth_request.json()

        self.auth_rest_util.headers['Signature'] = self.sign_cryptoutil.json_sign(full_request_json)
        print(self.auth_rest_util.headers['Signature'])
        self.auth_rest_util.headers['Authorization'] = 'Authorization=' + self.oidc_rest_util.perform().json()['access_token']
        self.auth_rest_util.data = full_request_json

        response = self.auth_rest_util.perform()
        return response.json()

if __name__=='authengine.authenticator':
    from dynaconf import Dynaconf
    settings = Dynaconf(settings_files=["config.toml"], envvar_prefix="TOKENSEEDER", environments=False)
else:
    from .. import settings

auth_rest_util = utils.RestUtility(
    settings.mosip_auth.ida_auth_url,
    method="POST",
    headers={
        "Authorization": "",
        "Signature": "",
        "content-type": "application/json",
    },
    data=''
)
oidc_token_rest_util = utils.RestUtility.oidc_rest_util(
    settings.mosip_auth.oidc_token_endpoint,
    settings.mosip_auth.partner_client_id,
    settings.mosip_auth.partner_client_secret,
    settings.mosip_auth.partner_username,
    settings.mosip_auth.partner_password
)
encrypt_cryptoutil = utils.CryptoUtility(
    settings.crypto.asymmetric_encrypt_public_key_path,
    None,
    symmetric_encrypt_key_size=settings.crypto.symmetric_encrypt_key_length,
    symmetric_encrypt_gcm_tag_length=settings.crypto.symmetric_encrypt_gcm_tag_length
)
sign_cryptoutil = utils.CryptoUtility(
    settings.crypto.sign_public_key_path,
    settings.crypto.sign_private_key_path,
    sign_algorithm=settings.crypto.sign_algorithm,
)
authenticator = MOSIPAuthenticator(
    auth_rest_util,
    settings.mosip_auth.ida_auth_domain_uri,
    encrypt_cryptoutil,
    sign_cryptoutil,
    settings.mosip_auth.partner_misp_lk,
    settings.mosip_auth.partner_client_id,
    settings.mosip_auth.partner_apikey,
    oidc_token_rest_util,
    settings.mosip_auth.ida_auth_version,
    settings.mosip_auth.ida_auth_request_id,
    settings.mosip_auth.ida_auth_env,
    settings.mosip_auth.timestamp_format,
)