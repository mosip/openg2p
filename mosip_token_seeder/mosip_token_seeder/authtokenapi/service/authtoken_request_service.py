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
        self.mapping_service = MappingService(config, logger)
        self.config = config
        self.db_engine = db_tools.db_init(config.db.location,password=config.db.password)
        self.logger = logger
        self.request_id_queue = request_id_queue
        
    def save_authtoken_json(self, request : AuthTokenRequest):
        
        language = request.lang
        if not request.lang:
            language = self.config.root.default_lang_code

        req_id = str(uuid.uuid4())

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
                auth_data_received = json.dumps(authdata),
            )
            valid_authdata, error_code = self.mapping_service.validate_auth_data(authdata, request.mapping, language)
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
                auth_data_received = json.dumps(authdata),
            )
            valid_authdata, error_code = self.mapping_service.validate_auth_data(authdata, request.mapping, language)
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
