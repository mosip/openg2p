import os
import requests

class RestUtility:
    def __init__(
        self,
        full_url,
        method="GET",
        headers={},
        data=None,
        cookies=None,
    ):
        self.url = full_url
        self.method = method
        self.headers = headers
        self.data = data
        self.cookies = cookies
    
    def perform(self):
        method_func = getattr(requests, self.method.lower(), requests.get)
        return method_func(
            self.url,
            headers = self.headers,
            data = self.data,
            cookies = self.cookies,
        )
    
    @classmethod
    def oidc_rest_util(cls, url, oidc_client_id, oidc_client_secret, oidc_username, oidc_password, method="POST", grant_type=None):
        rest_util = cls(
            url,
            method=method,
            headers={},
            data={}
        )
        if oidc_client_id:    
            rest_util.data['client_id'] = oidc_client_id
        if oidc_client_secret:
            rest_util.data['client_secret'] = oidc_client_secret
        if oidc_username:
            rest_util.data['username'] = oidc_username
        if oidc_password:
            rest_util.data['password'] = oidc_password
        if grant_type:
            rest_util.data['grant_type'] = grant_type
        else:
            if oidc_password:
                rest_util.data['grant_type'] = 'password'
            else:
                rest_util.data['grant_type'] = 'client_credentials'
        return rest_util
