import http
import json

from datetime import datetime
from typing import Union

from sqlalchemy import true

from mosip_token_seeder.authtokenapi.exception.mosip_token_seeder_exception import MOSIPTokenSeederException, MOSIPTokenSeederNoException

class ODKPullService:
    def __init__(self, logger):
        self.logger = logger
    
    def odk_pull(self, config):
        if not 'baseurl' in config or not len(config['baseurl']) :
                raise MOSIPTokenSeederException('ATS-REQ-18', 'no odk baseurl provided')

        if not 'email' in config or not len(config['email']) :
                raise MOSIPTokenSeederException('ATS-REQ-19', 'no email provided')

        if not 'password' in config or not len(config['password']) :
                raise MOSIPTokenSeederException('ATS-REQ-20', 'no password provided')
        
        credentials = {
            "email": config['email'],
            "password": config['password']
            }
        auth_url = 'https://{domain}/{version}/sessions'
        domain = config['baseurl'] 
        version = config['version'] if 'version' in config and len(config['version']) else 'v1'

        connection = http.client.HTTPSConnection(domain)
        headers = {'Content-type': 'application/json'} 
        connection.request(method='POST',url=auth_url.format(domain=domain,version=version), body = json.dumps(credentials),headers= headers)
        response = connection.getresponse()
        response_json_string = response.read().decode()
        auth_data =  json.loads(response_json_string)
        token = auth_data['token']

        if 'odataurl' in config and len(config['odataurl']):
            odata_url = config['odataurl']
            start_date = config['startdate'] if 'startdate' in config and len(config['startdate']) else None 
            end_date = config['enddate'] if 'enddate' in config and len(config['enddate']) else None
            

        else :
            if not 'baseurl' in config or not len(config['baseurl']) :
                raise MOSIPTokenSeederException('ATS-REQ-18', 'no odk baseurl provided')
            
            if not 'projectid' in config or not len(config['projectid']) :
                raise MOSIPTokenSeederException('ATS-REQ-19', 'no odk project id provided')
            
            if not 'formid' in config or not len(config['formid']) :
                raise MOSIPTokenSeederException('ATS-REQ-19', 'no odk form id provided')
            
        service_url = 'https://{domain}/{version}/projects/{projectid}/forms/{formid}.svc/Submissions'  
        if 'startdate' in config and len(config['startdate']) and 'enddate' in config and len(config['enddate']):
            filter = '?$filter=__system/submissionDate gt ' + config['startdate'] + ' and __system/submissionDate lt ' +  config['enddate']
            odata_url = odata_url + filter
        service_url.format(domain = domain, version = version, projectid = config['projectid'], formid = config['formid'])
        self.odk_pull_data(token, domain, service_url, start_date, end_date)
        auth_header = {'Authorization': 'Bearer ' + token}
        connection.request(method = "GET", url = odata_url, headers = auth_header)
        response = connection.getresponse()
        response_json_string = response.read().decode()
        print(response_json_string)
        submissions =  json.loads(response_json_string)
        if 'value' in submissions:
            return submissions['value']
        else :
            raise MOSIPTokenSeederException('ATS-REQ-20', 'no submissions found for odk pull')
            
        
        
        


        odata_url = config['odataurl']
        # 'https://odk.openg2p.mosip.net/v1/projects/1/forms/fourps_program.svc/Submissions'
