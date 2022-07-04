import os
import requests

class RestUtility:
    def __init__(self,url):
        self.url = url
    
    def get(self,headers={},data=None,cookies=None):
        return requests.get(
            self.url,
            headers = headers,
            data = data,
            cookies = cookies,
        )
    
    def post(self,headers={},data=None,cookies=None):
        return requests.post(
            self.url,
            headers = headers,
            data = data,
            cookies = cookies,
        )
