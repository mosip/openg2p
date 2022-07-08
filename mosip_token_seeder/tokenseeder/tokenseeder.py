from queue import Queue
from threading import Thread
from mosip_token_seeder.repository.db_tools import db_init

class TokenSeeder(Thread):
    def __init__(self, config, logger):
        self.queue = Queue()
        self.db_engine = db_init(config.db.location, config.db.password)
        self.logger = logger
    
    def run(self):
        while True:
            req_id = self.queue.get()
            