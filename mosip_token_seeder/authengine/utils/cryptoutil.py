import os
import base64
import json
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes, asymmetric, ciphers
from jwcrypto import jwk, jws

class CryptoUtility:
    def __init__(
        self,
        public_key_path,
        private_key_path,
        public_key_password=None,
        private_key_password=None,
        sign_algorithm = None,
        symmetric_encrypt_key_size=256,
        symmetric_encrypt_gcm_tag_length=128,
    ):
        self.public_key, self.public_cert, self.public_cert_pem_bytes = CryptoUtility.ret_pub_key_from_cert(public_key_path, public_key_password)
        self.private_key, self.private_key_jwk = CryptoUtility.ret_private_key(private_key_path, private_key_password)

        if self.public_cert:
            self.thumbprint = base64.urlsafe_b64encode(self.public_cert.fingerprint(hashes.SHA256()))
        else:
            self.thumbprint = None
        self.asymmetric_encrypt_padding = asymmetric.padding.OAEP(
            mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )

        self.symmetric_encrypt_key_size = symmetric_encrypt_key_size
        self.symmetric_encrypt_gcm_tag_length = symmetric_encrypt_gcm_tag_length
        self.sign_algorithm = sign_algorithm
    
    @staticmethod
    def ret_pub_key_from_cert(key_path, key_pass):
        if not key_path:
            return None
        with open(key_path, 'rb') as file:
            if key_path.endswith(".cert") or key_path.endswith(".crt"):
                pem_bytes = file.read()
                cert = x509.load_pem_x509_certificate(pem_bytes)
                return cert.public_key(), cert, pem_bytes
            else:
                return serialization.load_pem_public_key(file.read(), password=key_pass), None, None
    
    @staticmethod
    def ret_private_key(key_path, key_pass):
        if not key_path:
            return None, None
        with open(key_path, 'rb') as file:
            pem_bytes = file.read()
            return serialization.load_pem_private_key(pem_bytes, password=key_pass), jwk.JWK.from_pem(pem_bytes, password=key_pass)
    
    def asymmetric_encrypt(self, data):
        return self.public_key.encrypt(
            data,
            self.asymmetric_encrypt_padding
        )
    
    def symmetric_encrypt(self, data, key):
        iv = os.urandom(int(self.symmetric_encrypt_key_size/8))
        encryptor = ciphers.Cipher(
            ciphers.algorithms.AES(key),
            ciphers.modes.GCM(iv, tag=None, min_tag_length=int(self.symmetric_encrypt_gcm_tag_length/8)),
        ).encryptor()
        return encryptor.update(data) + encryptor.finalize() + iv
    
    def encrypt(self, data):
        data_bytes = data.encode('UTF-8')
        key = os.urandom(int(self.symmetric_encrypt_key_size/8))
        data_hash = hashes.Hash(hashes.SHA256())
        data_hash.update(data_bytes)
        request = base64.urlsafe_b64encode(self.symmetric_encrypt(data_bytes,key)).decode('UTF-8')
        encrypted_key = base64.urlsafe_b64encode(self.asymmetric_encrypt(key)).decode('UTF-8')
        hmac_digest = base64.urlsafe_b64encode(self.symmetric_encrypt(data_hash.finalize(),key)).decode('UTF-8')
        return request, encrypted_key, hmac_digest
    
    def json_sign(self, data):
        if not self.sign_algorithm:
             return None
        # return jws.sign(
        #     data.encode("UTF-8"),
        #     jwk.construct(self.private_key),
        #     headers={
        #         'x5c' : [base64.encodebytes(self.public_cert.public_bytes(serialization.Encoding.PEM)).decode("UTF-8")]
        #     },
        #     algorithm=self.sign_algorithm
        # )
        jwstoken = jws.JWS(data.encode('utf-8'))
        jwstoken.add_signature(self.private_key_jwk, None,
        json.dumps({"alg": self.sign_algorithm,"x5c":[base64.encodebytes(self.public_cert_pem_bytes).decode("UTF-8")]}),
        json.dumps({"kid": self.private_key_jwk.thumbprint()}))
        sig = jwstoken.serialize(compact=True).split('.')
        return sig[0] + ".." + sig[2]