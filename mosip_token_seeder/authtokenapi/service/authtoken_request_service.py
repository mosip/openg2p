from datetime import date, datetime
import json

from mosip_token_seeder.service.seeder_exception import SeederException
from ..model.authtoken_request_model import AuthTokenRequestModel
from ..model.authtoken_request_data_model import AuthTokenRequestDataModel
from ..repository.authtoken_request_repository import AuthTokenRequestRepository
from ..repository.authtoken_request_data_repository import AuthTokenRequestDataRepository
from .mapping_service import MappingService
import uuid

class AuthTokenService:
    def __init__(self) :
        self.auth_request_repository = AuthTokenRequestRepository()
        self.auth_request_data_repository = AuthTokenRequestDataRepository()
        self.mapper = MappingService()
    
    def save_authtoken_json(self,request_json):
        authtoken_request = AuthTokenRequestModel()
        if self.validate_json(request_json) == True :

            # call self.mapper(request_json)
            authtoken_request.auth_request_id = str(uuid.uuid1())
            
            authtoken_request.input_type = 'json'
            authtoken_request.output_type = request_json['output']
            authtoken_request.delivery_type = request_json['deliverytype']
            authtoken_request.status = 'submitted'
            authtoken_request.created_time =  date.today().strftime('%Y-%m-%d')

            self.auth_request_repository.add(authtoken_request)


            line_no = 0
            for authdata in request_json['authdata']:
                mapped_authdata = self.mapper.map_fields(authdata, request_json['mapping'] if 'mapping' in request_json else None)

                line_no = line_no + 1
                authdata_model = AuthTokenRequestDataModel()
                authdata_model.auth_request_id = authtoken_request.auth_request_id
                authdata_model.auth_request_line_no = line_no
                authdata_model.auth_data_recieved = json.dumps(authdata)
                authdata_model.auth_data_input = json.dumps(mapped_authdata)
                authdata_model.created_time =  date.today().strftime('%Y-%m-%d')
                authdata_model.status = 'submitted'

                self.auth_request_data_repository.add(authdata_model)
                
            return authtoken_request.auth_request_id 
    
    def __del__(self):
        # self.conn.close()
        pass

    def validate_json(self, request_json):

        # {
        #     "vid": "2014391641351279",
        #     "name": [{"language":"eng", "value": "EMANASAR-TEST-6"}],
        #     "gender": [{"language":"eng", "value": "Male"}],
        #     "dateOfBirth": "1976-01-01",
        #     "phoneNumber": "8360334018",
        #     "emailId": "PRASHANT.SINGH@IIITB.AC.IN",
        #     "fullAddress": [{"language":"eng", "value": "BANGALORE, Electronics City, Bengaluru, Karnataka, 560016"}]
        # }
        if 'authdata' not in  request_json :
            raise SeederException('ATH-STA-001','json is not in valid format ')

        if len(request_json['authdata']) == 0:
            raise SeederException('ATH-STA-001','json is not in valid format ')

        # is authdata valid

        mapping_required = True

        if 'mapping' not in  request_json :
            mapping_required = False
        elif len(request_json['mapping']) == 0: 
             mapping_required = False


        for authdata in request_json['authdata']:
            if mapping_required == False and ('vid' not in authdata or 'name' not in authdata or 'gender' not in authdata or'dateOfBirth' not in authdata or 'phoneNumber' not in authdata or'emailId' not in authdata or'fullAddress' not in authdata ):
                raise SeederException('ATH-STA-001','json is not in valid format ')
            elif mapping_required == True:
                if self.mapper.validate_map_fields(authdata, request_json['mapping']) == True:
                    authdata = self.mapper.map_fields(authdata,request_json['mapping'])

            if len(authdata['vid']) <= 16 and len(authdata['vid']) >= 19:
                raise SeederException('ATH-STA-002','invalid vid construct')

            if len(authdata['name']) == 0:
                raise SeederException('ATH-STA-003','name is not provided')

            if len(authdata['name']) > 256:
                 raise SeederException('ATH-STA-004','name is not provided')

            if len(authdata['gender']) == 0:
                raise Exception('gender is empty')

            if authdata['gender'].lower() not in ['male','female','others']:
                raise Exception('gender value is wrong')

            if len(authdata['dateOfBirth']) == 0:
                raise Exception('date of birth is empty')

            try:
                if bool(datetime.strptime(authdata['dateOfBirth'], '%Y-%m-%d')) == False :
                    raise Exception('not a valid date format for date of birth ')
            except ValueError:
                    raise Exception('not a valid date format for date of birth ')
            
            if len(authdata['fullAddress']) == 0:
                raise Exception('address is empty')
            

            return True
                
        