from datetime import date, datetime
import json
import logging
from os import stat

from .mosip_token_seeder_exception import MOSIPTokenSeederException
from ..model.authtoken_request_model import AuthTokenRequestModel
from ..model.authtoken_request_data_model import AuthTokenRequestDataModel
from mosip_token_seeder.repository.authtoken_request_repository import AuthTokenRequestRepository
from mosip_token_seeder.repository.authtoken_request_data_repository import AuthTokenRequestDataRepository
from .mapping_service import MappingService
import uuid

logger = logging.getLogger(__name__)
supported_output_types = ['json','csv']
supported_delivery_types = ['download']

class AuthTokenService:
    def __init__(self) :
        self.auth_request_repository = AuthTokenRequestRepository()
        self.auth_request_data_repository = AuthTokenRequestDataRepository()
        self.mapper = MappingService()
        
    def save_authtoken_json(self,request_json):
        authtoken_request = AuthTokenRequestModel()
        mapping_required = True

        if 'mapping' not in  request_json :
            mapping_required = False
        elif len(request_json['mapping']) == 0: 
             mapping_required = False
        language  = request_json['lang']
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
            error_count = 0
            for authdata in request_json['authdata']:

                is_valid_authdata, error_code = self.validate_auth_data(authdata, mapping_required, request_json['mapping'], language)
                if is_valid_authdata == True:    
                    mapped_authdata = self.mapper.map_fields(authdata, request_json['mapping'] if 'mapping' in request_json else None, language)
                    line_no += 1
                    authdata_model = AuthTokenRequestDataModel()
                    authdata_model.auth_request_id = authtoken_request.auth_request_id
                    authdata_model.auth_request_line_no = line_no
                    authdata_model.auth_data_recieved = json.dumps(authdata)
                    authdata_model.auth_data_input = json.dumps(mapped_authdata)
                    authdata_model.created_time =  date.today().strftime('%Y-%m-%d')
                    authdata_model.status = 'submitted'

                    self.auth_request_data_repository.add(authdata_model)
                else:
                    line_no +=1
                    error_count += 1
                    authdata_model = AuthTokenRequestDataModel()
                    authdata_model.auth_request_id = authtoken_request.auth_request_id
                    authdata_model.auth_request_line_no = line_no
                    authdata_model.auth_data_recieved = json.dumps(authdata)
                    authdata_model.created_time =  date.today().strftime('%Y-%m-%d')
                    authdata_model.status = 'invalid'
                    authdata_model.error_code = error_code

            if(error_count == line_no) :
                raise MOSIPTokenSeederException('ATS-REQ-101', 'none of the record form a valid request')
            else:
                return authtoken_request.auth_request_id 

    def fetch_status(self, request_identifier):
        status =  self.auth_request_repository.fetch_status(request_identifier)
        if status is None :
            raise MOSIPTokenSeederException('ATS-STA-002', 'no auth request found for the given identifier')
        return status

    def get_file(self, request_identifier):
        status =  self.auth_request_repository.fetch_status(request_identifier)
        output_json = []
        if status is None :
            raise MOSIPTokenSeederException('ATS-DWN-002', 'no auth request found for the given identifier')
        elif status != 'processed':
            raise MOSIPTokenSeederException('ATS-DWN-003', 'auth request not processed yet')
        else : 
            output_records = self.auth_request_data_repository.fetch_output(request_identifier)
            
           
            if(len(output_records) ==0) :
                raise MOSIPTokenSeederException('ATS-DWN-004', 'no records found')
            for output_record in output_records:
                print('output records',output_record[0])
                if(output_record[0] is not None):
                    output_json.append(json.loads(output_record[0]))
        if len(output_json) == 0 :
            raise MOSIPTokenSeederException('ATS-DWN-005', 'unable to locate any output geneated')
        return str.encode(json.dumps(output_json))


    def validate_json(self, request_json):
   
        if request_json["output"] is None:
            raise MOSIPTokenSeederException('ATS-REQ-020','output format not mentioned')
            
        if request_json["output"] not in supported_output_types:
            raise MOSIPTokenSeederException('ATS-REQ-021','output format not supported')

        if request_json["deliverytype"] is None:
            raise MOSIPTokenSeederException('ATS-REQ-022','delivery type not mentioned')

        if request_json["deliverytype"]  not in supported_delivery_types:
            raise MOSIPTokenSeederException('ATS-REQ-023','delivery type not supported')
        
        if 'authdata' not in  request_json :
            raise MOSIPTokenSeederException('ATS-REQ-001','json is not in valid format ')

        if len(request_json['authdata']) == 0:
            raise MOSIPTokenSeederException('ATS-REQ-001','json is not in valid format ')
        
        if 'authdata' not in  request_json :
            raise MOSIPTokenSeederException('ATS-REQ-001','json is not in valid format ')

        if len(request_json['authdata']) == 0:
            raise MOSIPTokenSeederException('ATS-REQ-001','json is not in valid format ')


        return True


    def validate_auth_data(self, authdata, mapping_required, mapping_json, language):
        if mapping_required == False and ('vid' not in authdata or 'name' not in authdata or 'gender' not in authdata or'dateOfBirth' not in authdata or 'phoneNumber' not in authdata or'emailId' not in authdata or'fullAddress' not in authdata ):
            return False, 'ATS-REQ-001'
        elif mapping_required == True:
            is_valid_data, error_code = self.mapper.validate_map_fields(authdata, mapping_json)
            if is_valid_data == True:
                authdata = self.mapper.map_fields(authdata,mapping_json, language)
            else: 
                return is_valid_data, error_code
       
        if len(authdata['vid']) <= 16 and len(authdata['vid']) >= 19:
            return False, 'ATS-REQ-002'

        if len(authdata['name']) == 0:
            return False, 'ATS-REQ-003'

        if len(authdata['name']) > 256:
            return False, 'ATS-REQ-003'

        if len(authdata['gender']) == 0:
            return False, 'ATS-REQ-004' 

        print("gender",authdata['gender'])
        if authdata['gender'][0]['value'].lower() not in ['male','female','others']:
            return False, 'ATS-REQ-005' 

        if len(authdata['dateOfBirth']) == 0:
            return False, 'ATS-REQ-006' 

        try:
            if bool(datetime.strptime(authdata['dateOfBirth'], '%Y-%m-%d')) == False :
                return False, 'ATS-REQ-007'
        except ValueError:
                return False, 'ATS-REQ-007' 
        
        if len(authdata['fullAddress']) == 0:
            return False, 'ATS-REQ-008' 
            
        return True,""
                
        