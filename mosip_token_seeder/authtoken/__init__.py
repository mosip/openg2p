from .. import app, settings

@app.get(settings.root.context_path + 'ping/auth')
def ping_auth():
    return "[" + str(settings.docker.pod_id) + ' - ' +  str(settings.gunicorn.worker_id) + "] auth"