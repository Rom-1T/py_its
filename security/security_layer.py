from encoder.encoding import security_foo, certificate_foo
import ecdsa
import hashlib
from security.certificate import get_certificate, decode_certificat
from ecdsa import SigningKey, VerifyingKey, SECP256k1, util, ellipticcurve

PSID = {
    "CAM" : 36,
    "DENM" : 37,
    "TLM" : 137,
    "RLT" : 139,
    "GNW" : 141,
    "SA" : 540801,
    "CRL" : 622,
    "CERTIFICATE_REQUEST" : 623,
    "CTL" : 624,
    "GPC" : 540802,
    "CP" : 639,
    "VRU" : 638,
    "TLC_REQUEST" : 140,
    "TLC_STATUS" : 637,
    "IMZ" : 640,
    "IVIM" : 139
}
class SecuredPacket :
    def __init__(self):
        self.data = {}

    def set_data(self, data):
        self.data = data

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.set_data(data)
        return instance

    @classmethod
    def from_encoded(cls, data):
        decoded = security_foo.decode("EtsiTs103097Data", data)
        return cls.from_dict(decoded)

    def encode(self):
        return security_foo.encode("EtsiTs103097Data", self.data)

    def upload_signed_payload(self, payload):
        if self.data["content"][0] == "signedData":
            print("update signed payload")
            # Retrieve the current 'content' tuple
            content_tuple = self.data["content"]
            # Retrieve the nested dictionary within the tuple
            nested_dict = content_tuple[1]
            # Navigate to the tuple you want to update
            inner_content_tuple = nested_dict["tbsData"]["payload"]["data"]["content"]
            # Update the tuple with the new payload value
            updated_inner_content_tuple = (inner_content_tuple[0], payload)
            # Update the nested dictionary with the new tuple
            nested_dict["tbsData"]["payload"]["data"]["content"] = updated_inner_content_tuple
            # Update the outer dictionary with the new nested dictionary
            self.data["content"] = (content_tuple[0], nested_dict)

class SecurityLayer:
    def __init__(self):
        self.identifier = "dfhsrthetkfdghh"
        self.key = None
        self.certificate = []
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        self.verifying_key = self.private_key.verifying_key
        self.root_ca = None
        self.ea_ca = None
        self.aa_ca = None

    def add_certificate(self, certificate):
        self.certificate.append(certificate)

    def add_key(self, key_string):
        self.private_key = ecdsa.SigningKey.from_string(key_string, curve=ecdsa.NIST256p, hashfunc=hashlib.sha256)

    def get_ca(self, url, type='root'):
        ca_certficate = decode_certificat(get_certificate(url))
        if ca_certficate is not None :
            if type == 'root' :
                self.root_ca = ca_certficate
            elif type == 'ea' :
                self.ea_ca = ca_certficate
            elif type == 'aa' :
                self.aa_ca = ca_certficate
            else :
                print("Wrong CA type")



    def get_pub_key(self):
        x_coordinate = self.verifying_key.pubkey.point.x()
        x_bytes = x_coordinate.to_bytes(32, byteorder='big')

        return ('ecdsaNistP256', ('x-only', x_bytes))

    def generate_signature(self, to_be_signed_data):
        # Sign a message
        signature = self.private_key.sign(to_be_signed_data, hashfunc=hashlib.sha256)

        # Extract R and S from the signature
        r, s = util.sigdecode_string(signature, self.private_key.curve.generator.order())

        # Encode R into x-only form
        r_bytes = r.to_bytes(32, byteorder='big')

        # Ensure s is 32 bytes
        s_bytes = s.to_bytes(32, byteorder='big')

        # Construct EcdsaP256Signature
        ecdsa_signature = {
            "rSig": ('x-only', r_bytes),  # EccP256CurvePoint
            "sSig": s_bytes,  # OCTET STRING (SIZE (32))
        }

        return ecdsa_signature

    def verify_signature(self, to_be_verified_data, signature):
        # Extract R and S from the signature
        r = int.from_bytes(signature["rSig"][1], 'big')
        s = int.from_bytes(signature["sSig"], 'big')

        # Construct the signature string
        signature_str = util.sigencode_string(r, s, self.verifying_key.pubkey.order)

        # Verify the signature
        try:
            self.verifying_key.verify(signature_str, to_be_verified_data, hashfunc=hashlib.sha256)
            return True
        except:
            return False

    def sign_its(self, its_message, common_header_gnw, payload_gnw, btp_packet, hash_algorithm='sha256'):
        psid = its_message.get_psid()
        tbs_data = common_header_gnw.encode() + payload_gnw.encode() + btp_packet + its_message.encode()

        return self._signe_its_packet_encoded(to_be_signed_data = tbs_data, hash_algorithm=hash_algorithm, psid = psid)

    def inner_ec_request(self):
        certificate_req_data = {
            'itsId': self.identifier.encode(),
            'certificateFormat': 1,
            'publicKeys': {
                'verificationKey': self.get_pub_key()
            },
            'requestedSubjectAttributes': {}
        }
        return certificate_foo.encode('InnerEcRequest', certificate_req_data)

    def _signe_its_packet_encoded(self, to_be_signed_data, hash_algorithm='sha256', psid=0):
        # TODO Integrate generation_delta_time
        generation_delta_time = 0
        signature = self.generate_signature(to_be_signed_data)

        if self.certificate:
            signer_data = ('certificate', self.certificate)
        else:
            signer_data = ('self', None)
        data = {
            'protocolVersion': 3,
            'content': ('signedData', {
                'hashId': hash_algorithm,
                'tbsData': {
                    'payload': {
                        'data': {
                            'protocolVersion': 3,
                            'content': (
                                'unsecuredData', to_be_signed_data
                            )
                        }
                    },
                    'headerInfo': {
                        'psid': psid,
                        'generationTime': 658095165660412,
                        'generationLocation' : {
                            'latitude' : 11111,
                            'longitude' : 222222,
                            'elevation' : 2222
                        }
                    }
                },
                'signer': signer_data,
                'signature': ('ecdsaNistP256Signature', signature)
            })
        }
        return security_foo.encode('Ieee1609Dot2Data', data)

    def certificate_request(self, certificate_request_packet):
        # TODO Integrate generation_delta_time
        generation_delta_time = 0
        signature = self.generate_signature(certificate_request_packet)

        first_layer_data = {
            'protocolVersion': 3,
            'content': ('signedData', {
                'hashId': 'sha256',
                'tbsData': {
                    'payload': {
                        'data': {
                            'protocolVersion': 3,
                            'content': (
                                'unsecuredData', certificate_request_packet
                            )
                        }
                    },
                    'headerInfo': {
                        'psid': PSID["CERTIFICATE_REQUEST"],
                        'generationTime': generation_delta_time
                    }
                },
                'signer': ('self', None),
                'signature': ('ecdsaNistP256Signature', signature)
            })
        }
        # first_layer = certificate_foo.encode('InnerEcRequestSignedForPop', first_layer_data)
        second_layer_data = {
            "version" : 1,
            "content" : ('enrolmentRequest',first_layer_data)
        }
        second_layer = certificate_foo.encode('EtsiTs102941Data', second_layer_data)

        signature_second_layer = self.generate_signature(second_layer)
        third_layer_data = {
            'protocolVersion': 3,
            'content': ('signedData', {
                'hashId': 'sha256',
                'tbsData': {
                    'payload': {
                        'data': {
                            'protocolVersion': 3,
                            'content': (
                                'unsecuredData', second_layer
                            )
                        }
                    },
                    'headerInfo': {
                        'psid': PSID["CERTIFICATE_REQUEST"],
                        'generationTime': generation_delta_time
                    }
                },
                'signer': ('self', None),
                'signature': ('ecdsaNistP256Signature', signature_second_layer)
            })
        }


        third_layer = certificate_foo.encode('EtsiTs103097Data', third_layer_data)
        return third_layer
