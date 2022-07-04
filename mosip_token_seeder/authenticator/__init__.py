from dynaconf import Dynaconf
from . import utils
from .authenticator import MOSIPAuthenticator

config = Dynaconf(settings_files=['config.toml','/app/token_seeder.conf'], envvar_prefix='TOKENSEEDER', environments=False)

auth_rest_util = utils.RestUtility(config.mosip_auth.ida_auth_url)
encrypt_cryptoutil = utils.CryptoUtility(**config.crypto.encrypt)
sign_cryptoutil = utils.CryptoUtility(**config.crypto.signature)

authenticator = MOSIPAuthenticator(
    auth_rest_util,
    encrypt_cryptoutil,
    sign_cryptoutil,
    **config.mosip_auth
)