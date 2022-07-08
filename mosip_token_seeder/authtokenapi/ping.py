class PingApi:
    def __init__(self, app, config, logger):
        @app.get(config.root.context_path + "ping")
        def ping():
            return "[%s - %s] pong" % (str(config.docker.pod_id), str(config.gunicorn.worker_id))