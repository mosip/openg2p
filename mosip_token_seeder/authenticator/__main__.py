import json
from dynaconf import Dynaconf
from authenticator import MOSIPAuthenticator

config = Dynaconf(settings_files=['authenticator-config.toml','/app/token_seeder.conf'], envvar_prefix='TOKENSEEDER', environments=False)

if __name__ == "__main__":
    mosip_authenticator = MOSIPAuthenticator(config)
    json_data = ''
    with open('samples/qrcod.json') as file:
        json_data = json.load(file)
    auth_resp = mosip_authenticator.do_auth(json_data)
    print (json.dumps(auth_resp))