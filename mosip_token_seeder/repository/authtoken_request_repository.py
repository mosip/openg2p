from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String



class AuthTokenRequestRepository:
    def __init__(self) :
        self.meta = MetaData()
        self.engine = create_engine('sqlite://', echo = True)
        self.auth_requests = Table(
            'auth_requests', self.meta, 
            Column('auth_request_id', String, primary_key = True), 
            Column('input_type', String), 
            Column('output_type', String),
            Column('delivery_type', String),
            Column('status', String),
            Column('created_time', String),
            Column('updated_time', String)
        )
        self.meta.create_all(self.engine)
        
    
    def add(self,authtokenrequest):

        insert_obj = self.auth_requests.insert().values(
            auth_request_id = authtokenrequest.auth_request_id, 
            input_type = authtokenrequest.input_type, 
            output_type = authtokenrequest.output_type, 
            delivery_type = authtokenrequest.delivery_type, 
            status = authtokenrequest.status, 
            created_time = authtokenrequest.created_time
        )
        conn = self.engine.connect()
        result = conn.execute(insert_obj)



    def update(self,authtokenrequest, auth_request_id):
        auth_request_id, input_type, output_type, delivery_type, status, created_time, updated_time = ""

        insert_query = """
        UPDATE "main"."auth_request"  SET 
                "input_type" = ?, 
                "output_type" ?, 
                "delivery_type" = ?, 
                "status" = ?, 
                "created_time" = ?, 
                "updated_time = ?"
            WHERE  "auth_request_id" = ?;
        """
        data_tuple = (auth_request_id, input_type, output_type, delivery_type, status, created_time, updated_time)
        self.dbsession.execute("UPDATE Person SET firstname=(\"Shibu\", lastname=\"Narayanan\" where id = 1")
        self.conn.commit()
    
