import sys
import json
from . import authenticator

available_subcommands = ['demoauth']

if len(sys.argv)<2 or sys.argv[1] not in available_subcommands:
    sys.exit('Available subcommands:\n\t%s' % '\n\t'.join(available_subcommands))
subcommand = sys.argv[1]
if subcommand == available_subcommands[0]:
    if len(sys.argv)<3:
        sys.exit('Usage:\n\tpython -m %s %s <data_json>' % ('authenticator',subcommand))
    print(authenticator.perform_demo_auth(json.loads(sys.argv[2])))