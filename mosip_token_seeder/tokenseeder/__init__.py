import uuid
import os

from .tokenseeder import TokenSeeder

def initialize(config, logger):
    return TokenSeeder(config, logger)