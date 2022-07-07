import json
from logging import exception
from multiprocessing.sharedctypes import Value

from sqlalchemy import true
from ..model.authtoken_request_model import AuthTokenRequestModel
from ..model.authtoken_base_model import AuthTokenBaseModel

class MappingService:
    def __init__(self) :
        pass
    
    def map_fields(self,authdata_json, mapping_json, language):
        mapped_auth_object = AuthTokenBaseModel()

        if 'vid' in authdata_json :
            mapped_auth_object.vid = authdata_json['vid']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'vid')
            mapped_auth_object.vid = self.get_mapped_value(authdata_json,mapped_field)
        
        if 'name' in authdata_json :
            mapped_auth_object.name = [{"language" : language, "value": authdata_json['name']}]
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'name')
            mapped_auth_object.name = [{"language" : language, "value": self.get_mapped_value(authdata_json,mapped_field)}]
        
        if 'gender' in authdata_json :
            mapped_auth_object.gender = [{"language" : language, "value": authdata_json['gender']}]
        else :
            mapped_field = [{"language" : language, "value": self.get_mapped_field(mapping_json, 'gender')}]
            mapped_auth_object.gender = [{"language" : language, "value": self.get_mapped_value(authdata_json,mapped_field)}]

        if 'dateOfBirth' in authdata_json :
            mapped_auth_object.dateOfBirth = authdata_json['dateOfBirth']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'dateOfBirth')
            mapped_auth_object.dateOfBirth = self.get_mapped_value(authdata_json,mapped_field)
            
        if 'phoneNumber' in authdata_json :
            mapped_auth_object.phoneNumber = authdata_json['phoneNumber']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'phoneNumber')
            mapped_auth_object.phoneNumber = self.get_mapped_value(authdata_json,mapped_field)
            
        if 'emailId' in authdata_json :
            mapped_auth_object.emailId = authdata_json['emailId']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'emailId')
            mapped_auth_object.emailId = self.get_mapped_value(authdata_json,mapped_field)

        if 'fullAddress' in authdata_json :
            mapped_auth_object.fullAddress = [{"language" : language, "value": authdata_json['fullAddress']}]
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'fullAddress')
            mapped_auth_object.fullAddress = [{"language" : language, "value": self.get_mapped_value(authdata_json,mapped_field)}]
            
        return json.loads(mapped_auth_object.json())


    def validate_map_fields(self,authdata_json, mapping_json):
        if 'vid' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'vid')
            if mapped_field is None:
                return False, 'ATS-REQ-009'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-009'
        
        if 'name' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'name')
            if mapped_field is None:
                return False, 'ATS-REQ-010'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-010'
        
        if 'gender' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'gender')
            if mapped_field is None:
               return False, 'ATS-REQ-011'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-011'

        if 'dateOfBirth' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'dateOfBirth')
            if mapped_field is None:
                return False, 'ATS-REQ-012'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-012'
        
        if 'phoneNumber' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'phoneNumber')
            if mapped_field is None:
                return False, 'ATS-REQ-013'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-013'

        if 'emailId' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'emailId')
            if mapped_field is None:
                return False, 'ATS-REQ-014'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-014'

        if 'fullAddress' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'fullAddress')
            if mapped_field is None:
                return False, 'ATS-REQ-015'
            elif self.is_valid_mapped_field(authdata_json,mapped_field) == False:
                return False, 'ATS-REQ-015'

        return True, ''


    def get_mapped_field(self, mapping_json,field_name):
        output = None
        if field_name in mapping_json:
            output = mapping_json[field_name]   
        return output


    def get_mapped_value(self,auth_data, mapped_field):
        output = None
        if isinstance(mapped_field, list):
            # delimiter = mapped_field['delimiter'] if 'delimiter' in mapped_field else ' '
            delimiter = ' '
            output = ""
            for field_item in mapped_field:
                if field_item in auth_data:
                    output = output + auth_data[field_item] + delimiter
            output = output.strip(delimiter)
        else:
            output = auth_data[mapped_field]
        
        # if output != None and  mapped_field["withLangCode"] == true :
        #     lang = auth_data["lang"] if "lang" in  auth_data else "eng"
        #     output = [{'language': lang, 'value': output}]
            
        return output


    def is_valid_mapped_field(self,auth_data,mapped_field):
        output = True
        if isinstance(mapped_field, list):
            for field_item in mapped_field:
                if field_item not in auth_data:
                    output = False
                    break
        elif mapped_field not in auth_data:
                output = False
        output
