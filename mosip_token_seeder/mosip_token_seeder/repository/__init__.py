from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()

class ExtendedBase:

    def add_to_session(self, session : Session):
        session.add(self)
        return self
    
    def add(self, engine):
        with Session(engine) as session:
            session.expire_on_commit = False
            self.add_to_session(session)
            session.commit()
            
        return self
    
    def update_change(self, session : Session):
        self.upd_dtimes = datetime.utcnow()
        session.commit()

from .authtoken_request_data_repository import AuthTokenRequestDataRepository
from .authtoken_request_repository import AuthTokenRequestRepository