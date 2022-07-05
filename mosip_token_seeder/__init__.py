#from msilib import schema
import os
from pydoc import describe
import traceback
from unicodedata import name
from fastapi import FastAPI
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=[os.path.join(__name__,"config.toml"), "/app/token_seeder.conf"], envvar_prefix="TOKENSEEDER", environments=False)
description = """
MOSIP Token Seeder API is a toolkit for generating MOSIP token for the enrolled users

***********************************
Further details goes here 
***********************************
"""
app = FastAPI(
    title="MOSIP Token Seeder",
    version='0.1.0',
    description=description,
    contact={
        "url": "https://mosip.io/contact.php",
        "email": "info@mosip.io",
    },
    license_info={
        "name":"Mozilla Public License 2.0",
        "url": "https://www.mozilla.org/en-US/MPL/2.0/",
    },


)

@app.get(config.root.context_path + "ping")
def ping():
    return "[" + str(config.docker.pod_id) + ' - ' +  str(config.gunicorn.worker_id) + "] pong"

def get_current_worker_id(config):
    if config.root.pid_grep_name=='local':
        return
    import subprocess
    try:
        pid_arr = sorted([int(a) for a in str(subprocess.check_output(['pgrep','-f',config.root.pid_grep_name]), 'UTF-8').split('\n') if a])
        config.gunicorn.worker_id = pid_arr.index(os.getpid()) - 1
    except:
        config.gunicorn.worker_id = -1

def get_pod_id(config):
    config.docker.pod_id = int(config.docker.pod_name.split('-')[-1])

    get_current_worker_id(config)
    get_pod_id(config)

from . import authenticator
from . import tokenseeder
from . import authtoken
from .authtoken import token_seeder
