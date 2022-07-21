import codecs
import csv
import json
import logging
from typing import List, Union
import uuid

from datetime import date, datetime

from fastapi import UploadFile

from ..model import AuthTokenRequest, MapperFields, MapperFieldIndices, AuthTokenBaseModel
from ..model import AuthTokenCsvRequest, AuthTokenCsvRequestWithHeader, AuthTokenCsvRequestWithoutHeader
from ..exception import MOSIPTokenSeederNoException
from mosip_token_seeder.repository import AuthTokenRequestRepository, AuthTokenRequestDataRepository
from mosip_token_seeder.repository import db_tools
from . import MappingService


class AuthTokenService:
    def __init__(self, config, logger, request_id_queue) :
        # self.mapper = MappingService()
        self.config = config
        self.db_engine = db_tools.db_init(config.db.location,password=config.db.password)
        self.logger = logger
        self.request_id_queue = request_id_queue
        
    def save_authtoken_json(self, request : AuthTokenRequest):
        # authtoken_request = AuthTokenRequestModel()
        # mapping_required = True

        # if not request.mapping:
        #     mapping_required = False
        
        language = request.lang
        if not request.lang:
            language = self.config.root.default_lang_code

        req_id = str(uuid.uuid4())

        # call self.mapper(request_json)
        authtoken_request_entry = AuthTokenRequestRepository(
            auth_request_id = req_id,
            number_total = len(request.authdata),
            input_type = 'json',
            output_type = request.output,
            delivery_type = request.deliverytype,
            status = 'submitted'
        )

        line_no = 0
        error_count = 0
        for authdata in request.authdata:
            line_no += 1
            authdata_model = AuthTokenRequestDataRepository(
                auth_request_id = req_id,
                auth_request_line_no = line_no,
                auth_data_recieved = json.dumps(authdata),
            )
            valid_authdata, error_code = self.validate_auth_data(authdata, request.mapping, language)
            if valid_authdata:
                authdata_model.auth_data_input = valid_authdata.json()
                authdata_model.status = 'submitted'
            else:
                error_count += 1
                authdata_model.status = 'invalid'
                authdata_model.error_code = error_code
            authdata_model.add(self.db_engine)
        
        authtoken_request_entry.number_error = error_count

        if(error_count == line_no) :
            authtoken_request_entry.status = 'submitted_with_errors'
            authtoken_request_entry.add(self.db_engine)
            self.request_id_queue.put(req_id)
            raise MOSIPTokenSeederNoException('ATS-REQ-101', 'none of the record form a valid request', 200, response={
                'request_identifier': req_id
            })
        
        authtoken_request_entry.add(self.db_engine)
        self.request_id_queue.put(req_id)
        return req_id
    
    def save_authtoken_csv(self, request : AuthTokenCsvRequest, csv_file : UploadFile):
        language = request.lang
        if not request.lang:
            language = self.config.root.default_lang_code

        req_id = str(uuid.uuid4())

        if isinstance(request, AuthTokenCsvRequestWithHeader):
            with_header = True
            csv_header = None
        elif isinstance(request, AuthTokenCsvRequestWithoutHeader):
            with_header = False
        
        line_no = 0
        error_count = 0
        csv_reader = csv.reader(codecs.iterdecode(csv_file.file,'UTF-8'), delimiter=request.csvDelimiter)
        for csv_line in csv_reader:
            if with_header and line_no==0 and not csv_header:
                csv_header = csv_line
                continue
            elif with_header:
                authdata = { column_name: csv_line[i] for i, column_name in enumerate(csv_header) }
            elif not with_header:
                authdata = csv_line
            line_no += 1
            
            authdata_model = AuthTokenRequestDataRepository(
                auth_request_id = req_id,
                auth_request_line_no = line_no,
                auth_data_recieved = json.dumps(authdata),
            )
            valid_authdata, error_code = self.validate_auth_data(authdata, request.mapping, language)
            if valid_authdata:
                authdata_model.auth_data_input = valid_authdata.json()
                authdata_model.status = 'submitted'
            else:
                error_count += 1
                authdata_model.status = 'invalid'
                authdata_model.error_code = error_code
            authdata_model.add(self.db_engine)
        
        authtoken_request_entry = AuthTokenRequestRepository(
            auth_request_id = req_id,
            number_total = line_no,
            input_type = 'csv',
            output_type = request.output,
            delivery_type = request.deliverytype,
            status = 'submitted',
            number_error = error_count,
        )

        if(error_count == line_no) :
            authtoken_request_entry.status = 'submitted_with_errors'
            authtoken_request_entry.add(self.db_engine)
            self.request_id_queue.put(req_id)
            raise MOSIPTokenSeederNoException('ATS-REQ-101', 'none of the record form a valid request', 200,response={
                'request_identifier': req_id
            })
        
        authtoken_request_entry.add(self.db_engine)
        self.request_id_queue.put(req_id)
        return req_id

    def fetch_status(self, request_identifier):
        try:
            status = AuthTokenRequestRepository.fetch_status(request_identifier, self.db_engine)
        except Exception as e:
            raise MOSIPTokenSeederNoException('ATS-REQ-016', 'no auth request found for the given identifier', 404)
        if not status:
            raise MOSIPTokenSeederNoException('ATS-REQ-016', 'no auth request found for the given identifier', 404)
        return status

    def assert_download_status(self, request_identifier):
        status =  self.fetch_status(request_identifier)
        if not status.startswith('processed'):
            raise MOSIPTokenSeederNoException('ATS-REQ-017', 'Auth request not processed yet', 202)

    def validate_auth_data(self, authdata, mapping: Union[MapperFields, MapperFieldIndices], language):
        if isinstance(mapping, MapperFields):
            return self.validate_auth_data_json_mapper(authdata, mapping, language)
        elif isinstance(mapping, MapperFieldIndices):
            return self.validate_auth_data_indices_mapper(authdata, mapping, language)
    
    def validate_auth_data_json_mapper(self, authdata : dict, mapping: MapperFields, language):
        final_dict = {}
        if mapping.vid not in authdata:
            return None, 'ATS-REQ-009'
        if len(authdata[mapping.vid]) <= 16 and len(authdata[mapping.vid]) >= 19:
            return None, 'ATS-REQ-002'
        final_dict['vid'] = authdata[mapping.vid]

        name_arr = []
        for name_var in mapping.name:
            if name_var not in authdata:
                return None, 'ATS-REQ-010'
            if len(authdata[name_var]) == 0:
                return None, 'ATS-REQ-003'
            name_arr.append(authdata[name_var])
        final_dict['name'] = [{'language':language,'value': self.config.root.name_delimiter.join(name_arr)}]

        if mapping.gender not in authdata:
            return None, 'ATS-REQ-011'
        if len(authdata[mapping.gender]) > 256:
            return None, 'ATS-REQ-003'
        if len(authdata[mapping.gender]) == 0:
            return None, 'ATS-REQ-004'
        if authdata[mapping.gender].lower() not in ['male','female','others']:
            return None, 'ATS-REQ-005' 
        final_dict['gender'] = [{'language':language,'value': authdata[mapping.gender]}]

        if mapping.dob not in authdata:
            return None, 'ATS-REQ-012'
        if len(authdata[mapping.dob]) == 0:
            return False, 'ATS-REQ-006'
        try:
            if bool(datetime.strptime(authdata[mapping.dob], '%Y/%m/%d')) == False:
                return None, 'ATS-REQ-007'
        except ValueError:
            return None, 'ATS-REQ-007'
        final_dict['dob'] = authdata[mapping.dob]
        
        if mapping.phoneNumber not in authdata:
            return None, 'ATS-REQ-013'
        final_dict['phoneNumber'] = authdata[mapping.phoneNumber]
        if mapping.emailId not in authdata:
            return None, 'ATS-REQ-014'
        final_dict['emailId'] = authdata[mapping.emailId]

        addr_arr = []
        for addr in mapping.fullAddress:
            if addr not in authdata:
                return None, 'ATS-REQ-015'
            if len(authdata[addr]) == 0:
                return False, 'ATS-REQ-008'
            addr_arr.append(authdata[addr])
        final_dict['fullAddress'] = [{'language':language,'value': self.config.root.full_address_delimiter.join(addr_arr)}]
        return AuthTokenBaseModel(**final_dict),""

    def validate_auth_data_indices_mapper(self, authdata : list, mapping: MapperFieldIndices, language):
        final_dict = {}
        len_of_authdata = len(authdata)
        if mapping.vid >= len_of_authdata:
            return None, 'ATS-REQ-009'
        if len(authdata[mapping.vid]) <= 16 and len(authdata[mapping.vid]) >= 19:
            return None, 'ATS-REQ-002'
        final_dict['vid'] = authdata[mapping.vid]

        name_arr = []
        for name_index in mapping.name:
            if name_index >= len_of_authdata:
                return None, 'ATS-REQ-010'
            if len(authdata[name_index]) == 0:
                return None, 'ATS-REQ-003'
            name_arr.append(authdata[name_index])
        final_dict['name'] = [{'language':language,'value': self.config.root.name_delimiter.join(name_arr)}]

        if mapping.gender >= len_of_authdata:
            return None, 'ATS-REQ-011'
        if len(authdata[mapping.gender]) > 256:
            return None, 'ATS-REQ-003'
        if len(authdata[mapping.gender]) == 0:
            return None, 'ATS-REQ-004'
        if authdata[mapping.gender].lower() not in ['male','female','others']:
            return None, 'ATS-REQ-005'
        final_dict['gender'] = [{'language':language,'value': authdata[mapping.gender]}]

        if mapping.dob >= len_of_authdata:
            return None, 'ATS-REQ-012'
        if len(authdata[mapping.dob]) == 0:
            return False, 'ATS-REQ-006'
        try:
            if bool(datetime.strptime(authdata[mapping.dob], '%Y/%m/%d')) == False:
                return None, 'ATS-REQ-007'
        except ValueError:
            return None, 'ATS-REQ-007'
        final_dict['dob'] = authdata[mapping.dob]
        
        if mapping.phoneNumber >= len_of_authdata:
            return None, 'ATS-REQ-013'
        final_dict['phoneNumber'] = authdata[mapping.phoneNumber]
        if mapping.emailId >= len_of_authdata:
            return None, 'ATS-REQ-014'
        final_dict['emailId'] = authdata[mapping.emailId]

        addr_arr = []
        for addr_index in mapping.fullAddress:
            if addr_index >= len_of_authdata:
                return None, 'ATS-REQ-015'
            if len(authdata[addr_index]) == 0:
                return False, 'ATS-REQ-008'
            addr_arr.append(authdata[addr_index])
        final_dict['fullAddress'] = [{'language':language,'value': self.config.root.full_address_delimiter.join(addr_arr)}]
        return AuthTokenBaseModel(**final_dict),""
