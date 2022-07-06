from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

class AuthTokenRequestDataRepository:
    def __init__(self) :

        self.meta = MetaData()
        self.engine = create_engine('sqlite://', echo = True)
        self.auth_request_data = Table(
            'auth_request_data', self.meta, 
            Column('auth_request_id', String, primary_key = True), 
            Column('auth_request_line_no',Integer, primary_key=True),
            Column('auth_data_recieved', String), 
            Column('auth_data_input', String),
            Column('auth_data_output', String),
            Column('token', String),
            Column('error_code', String),
            Column('status', String),
            Column('created_time', String),
            Column('updated_time', String)
        )
        self.meta.create_all(self.engine)
        
    
    def add(self,authtoken_request_data):

        insert_obj = self.auth_request_data.insert().values(
            auth_request_id = authtoken_request_data.auth_request_id, 
            auth_request_line_no = authtoken_request_data.auth_request_line_no,
            auth_data_recieved = authtoken_request_data.auth_data_recieved, 
            auth_data_input = authtoken_request_data.auth_data_input, 
            auth_data_output = authtoken_request_data.auth_data_output, 
            token = authtoken_request_data.token,
            status = authtoken_request_data.status, 
            created_time = authtoken_request_data.created_time
        )
        conn = self.engine.connect()
        result = conn.execute(insert_obj)

        
    # def __del__(self):
    #     self.conn.close()