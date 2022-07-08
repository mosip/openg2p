from .authenticator import MOSIPAuthenticator


def initialize(app, config, logger):
    authenticator = MOSIPAuthenticator(config,logger)
    return authenticator