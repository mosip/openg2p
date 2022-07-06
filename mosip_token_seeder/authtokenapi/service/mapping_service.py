import json
from logging import exception
from ..model.authtoken_request_model import AuthTokenRequestModel
from ..model.authtoken_base_model import AuthTokenBaseModel

class MappingService:
    def __init__(self) :
        pass
    
    def map_fields(self,authdata_json, mapping_json):
        # Mapping code goes here
      
        mapped_auth_object = AuthTokenBaseModel()

        if 'vid' in authdata_json :
            mapped_auth_object.vid = authdata_json['vid']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'vid')
            mapped_auth_object.vid = authdata_json[mapped_field]
            

        
        if 'name' in authdata_json :
            mapped_auth_object.name = authdata_json['name']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'name')
            mapped_auth_object.name = authdata_json[mapped_field]
          

        
        if 'gender' in authdata_json :
            mapped_auth_object.gender = authdata_json['gender']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'gender')
            mapped_auth_object.gender = authdata_json[mapped_field]
            

        if 'dateOfBirth' in authdata_json :
            mapped_auth_object.dateOfBirth = authdata_json['dateOfBirth']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'dateOfBirth')
            mapped_auth_object.dateOfBirth = authdata_json[mapped_field]
            
        
        if 'phoneNumber' in authdata_json :
            mapped_auth_object.phoneNumber = authdata_json['phoneNumber']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'phoneNumber')
            mapped_auth_object.phoneNumber = authdata_json[mapped_field]
            
    

        if 'emailId' in authdata_json :
            mapped_auth_object.emailId = authdata_json['emailId']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'emailId')
            mapped_auth_object.emailId = authdata_json[mapped_field]
           


        if 'fullAddress' in authdata_json :
            mapped_auth_object.fullAddress = authdata_json['fullAddress']
        else :
            mapped_field = self.get_mapped_field(mapping_json, 'fullAddress')
            mapped_auth_object.fullAddress = authdata_json[mapped_field]
            
        return json.loads(mapped_auth_object.json())

    def validate_map_fields(self,authdata_json, mapping_json):

        mapped_auth_object = AuthTokenBaseModel()
       

        if 'vid' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'vid')
            if mapped_field == None:
                return False, 'ATS-REQ-009'
            elif mapped_field not in authdata_json:
                print(authdata_json)
                print(mapped_field)
                return False, 'ATS-REQ-009'

        
        if 'name' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'name')
            if mapped_field == None:
                return False, 'ATS-REQ-010'
            elif mapped_field not in authdata_json:
                return False, 'ATS-REQ-010'


        
        if 'gender' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'gender')
            if mapped_field == None:
               return False, 'ATS-REQ-011'
            elif mapped_field not in authdata_json:
                return False, 'ATS-REQ-011'

        if 'dateOfBirth' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'dateOfBirth')
            if mapped_field == None:
                return False, 'ATS-REQ-012'
            elif mapped_field not in authdata_json:
                return False, 'ATS-REQ-012'

        
        if 'phoneNumber' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'phoneNumber')
            if mapped_field == None:
                return False, 'ATS-REQ-013'
            elif mapped_field not in authdata_json:
                return False, 'ATS-REQ-013'
    

        if 'emailId' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'emailId')
            if mapped_field == None:
                return False, 'ATS-REQ-014'
            elif mapped_field not in authdata_json:
                return False, 'ATS-REQ-014'


        if 'fullAddress' not in authdata_json :
            mapped_field = self.get_mapped_field(mapping_json, 'fullAddress')
            if mapped_field == None:
                return False, 'ATS-REQ-015'
            elif mapped_field not in authdata_json:
                return False, 'ATS-REQ-015'

        return True

        
    def get_mapped_field(self, mapping_json,field):
        
        output = None
        for map_field in mapping_json:
            if(map_field['authfield'] == field) :
               
                output = map_field['mappingfield']   
                break
        return output

    
    def __del__(self):
        pass