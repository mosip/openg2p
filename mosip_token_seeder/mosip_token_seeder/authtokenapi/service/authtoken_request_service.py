import json
import logging
import uuid

from datetime import date, datetime

from ..model import AuthTokenRequest
from ..exception import MOSIPTokenSeederException, MOSIPTokenSeederNoException
from mosip_token_seeder.repository import AuthTokenRequestRepository, AuthTokenRequestDataRepository
from mosip_token_seeder.repository import db_tools
from . import MappingService


class AuthTokenService:
    def __init__(self, config, logger, request_id_queue) :
        self.mapper = MappingService()
        self.config = config
        self.db_engine = db_tools.db_init(config.db.location,password=config.db.password)
        self.logger = logger
        self.request_id_queue = request_id_queue
        
    def save_authtoken_json(self, request : AuthTokenRequest):
        # authtoken_request = AuthTokenRequestModel()
        mapping_required = True

        if not request.mapping:
            mapping_required = False
        
        language = request.lang
        if not request.lang:
            language = self.config.root.default_lang_code

        # call self.mapper(request_json)
        authtoken_request_entry = AuthTokenRequestRepository(
            auth_request_id = str(uuid.uuid4()),
            number_total = len(request.authdata),
            input_type = 'json',
            output_type = request.output,
            delivery_type = request.deliverytype,
            status = 'submitted'
        )

        authtoken_request_entry.add(self.db_engine)

        line_no = 0
        error_count = 0
        for authdata in request.authdata:
            line_no += 1
            authdata_model = AuthTokenRequestDataRepository(
                auth_request_id = authtoken_request_entry.auth_request_id,
                auth_request_line_no = line_no,
                auth_data_recieved = json.dumps(authdata),
            )
            is_valid_authdata, error_code = self.validate_auth_data(authdata, mapping_required, request.mapping, language)
            if is_valid_authdata == True:    
                authdata_model.auth_data_input = self.mapper.map_fields(authdata, request.mapping, language)
                authdata_model.status = 'submitted'
            else:
                error_count += 1
                authdata_model.status = 'invalid'
                authdata_model.error_code = error_code
            authdata_model.add(self.db_engine)
        
        self.request_id_queue.put(authtoken_request_entry.auth_request_id)

        if(error_count == line_no) :
            raise MOSIPTokenSeederException('ATS-REQ-101', 'none of the record form a valid request')
        else:
            return authtoken_request_entry.auth_request_id 

    def fetch_status(self, request_identifier):
        try:
            status = AuthTokenRequestRepository.fetch_status(request_identifier)
        except Exception as e:
            raise MOSIPTokenSeederNoException('ATS-REQ-016', 'no auth request found for the given identifier', 404)
        if not status:
            raise MOSIPTokenSeederNoException('ATS-REQ-016', 'no auth request found for the given identifier', 404)
        return status

    def assert_download_status(self, request_identifier):
        status =  self.fetch_status(request_identifier, self.db_engine)
        if status != 'processed':
            raise MOSIPTokenSeederNoException('ATS-REQ-017', 'Auth request not processed yet', 202)

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

        if authdata['gender'].lower() not in ['male','female','others']:
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
                
        