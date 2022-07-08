import os
import sys
from . import db_init
from dynaconf import Dynaconf

config = Dynaconf(settings_files=["config.toml","/app/token_seeder.conf"], envvar_prefix="TOKENSEEDER", environments=False)

available_subcommands = ['dbinit']

if len(sys.argv)<2 or sys.argv[1] not in available_subcommands:
    sys.exit('Available subcommands:\n\t%s' % '\n\t'.join(available_subcommands))
subcommand = sys.argv[1]
if subcommand == available_subcommands[0]:
    if len(sys.argv)>3:
        sys.exit('Usage:\n\tpython -m %s %s' % ('tokenseeder',subcommand))
    if config.db.get('generate_db_always',True):
        username = config.db.username
        password = config.db.password
        location = config.db.location
        if config.db.get('generate_password_always',True):
            password = db_init.generate_password(config.db.random_password_length)
        location = location.replace('<username>',username)
        location = location.replace('<password>',password)
        eng = db_init.db_init(location)
        db_init.db_create(eng)
        print(password)