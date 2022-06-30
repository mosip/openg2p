import sys
import json
from .authenticator import authenticator

if len(sys.argv)<2:
    print('Available subcommands:\n\tauthenticator')
elif sys.argv[1] == "authenticator":
    if len(sys.argv)<3:
        print('Usage:\n\tpython -m authengine authenticator <data_json>')
        exit(1)
    print(authenticator.perform_demo_auth(json.loads(sys.argv[2])))