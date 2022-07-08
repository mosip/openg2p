import os

import mosip_token_seeder

from mosip_token_seeder import authenticator, authtokenapi, tokenseeder

config = mosip_token_seeder.init_config()
app = mosip_token_seeder.init_app(config)
logger = mosip_token_seeder.init_logger(config)

mosip_authenticator = authenticator.initialize(config, logger)
token_seeder = tokenseeder.initialize(config, logger)
authtokenapi.initialize(app, config, logger, token_seeder.request_id_queue)