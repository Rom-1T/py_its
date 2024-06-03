from ITS.ethernet import Ethernet
from ITS.geonet.geonet_layer import BasicHeader, CommonHeader, Beacon, GeoUniCast, GeoBroadCast, TopologicalBroadcast, \
    SingleHopeBroadcast
from ITS.btp import BTP
from ITS.its import CAM, DENM, IVIM
from security.security_layer import SecuredPacket
from encoder.encoding import security_foo


class ItsMessage:
    def __init__(self):
        self._ethernet = None
        self._basic_header = None
        self._secured_header = None
        self._common_header = None
        self._extended_header = None
        self._btp = None
        self._its = None

    @property
    def ethernet(self):
        return self._ethernet

    @ethernet.setter
    def ethernet(self, ethernet: Ethernet):
        self._ethernet = ethernet

    @property
    def basic_header(self):
        return self._basic_header

    @basic_header.setter
    def basic_header(self, basic_header):
        self._basic_header = basic_header

    @property
    def common_header(self):
        return self._common_header

    @common_header.setter
    def common_header(self, common_header):
        self._common_header = common_header

    @property
    def secured_header(self):
        return self._secured_header

    @secured_header.setter
    def secured_header(self, secured_header):
        self._secured_header = secured_header

    @property
    def extended_header(self):
        return self._extended_header

    @extended_header.setter
    def extended_header(self, extended_header):
        self._extended_header = extended_header

    @property
    def btp(self):
        return self._btp

    @btp.setter
    def btp(self, btp):
        self._btp = btp

    @property
    def its(self):
        return self._its

    @its.setter
    def its(self, its):
        self._its = its  # Fixing the recursive setting

    @classmethod
    def decode(cls, encoded_data):
        try :
            instance = cls()
            ethernet = Ethernet.decode(encoded_data[0:14])
            basic_header = BasicHeader.from_encoded(encoded_data[14:18])

            if basic_header.data["versionAndNextHeader"]["nextHeader"] == 2:
                secured_header = SecuredPacket.from_encoded(encoded_data[18:])
                instance.secured_header = secured_header
                secured_content_type = secured_header.data["content"][0]

                if secured_content_type == 'signedData':
                    common_payload = secured_header.data["content"][1]["tbsData"]["payload"]["data"]["content"][1]
                elif secured_content_type == 'unsecuredData':
                    common_payload = secured_header.data["content"][1]
                elif secured_content_type == 'encryptedData':
                    print("Decrypt has not been implemented yet")
                    return instance
            else:
                common_payload = encoded_data[18:]

            common_header = CommonHeader.from_encoded(common_payload[:8])
            header_type = common_header.data["headerType"]["type"]
            sub_type = common_header.data["headerType"]["subType"]

            if header_type == 1:
                extended = Beacon.from_encoded(common_payload[8:])
            elif header_type == 2:
                extended = GeoUniCast.from_encoded(common_payload[8:])
            elif header_type == 3 or header_type == 4:
                extended = GeoBroadCast.from_encoded(common_payload[8:])
            elif header_type == 5 and sub_type == 0:
                extended = SingleHopeBroadcast.from_encoded(common_payload[8:])
            elif header_type == 5 and sub_type == 1:
                extended = TopologicalBroadcast.from_encoded(common_payload[8:])

            btp = BTP.decode(common_payload[8 + extended.size:8 + extended.size + 4])

            its_type = btp.interpret_port()

            if its_type == "CAM":
                its = CAM.from_encoded(common_payload[8 + extended.size + 4:])
            elif its_type == "DENM":
                its = DENM.from_encoded(common_payload[8 + extended.size + 4:])
            elif its_type == "IVIM":
                its = IVIM.from_encoded(common_payload[8 + extended.size + 4:])
            else:
                its = None
                print("Unknown message type : ", its_type)
            instance.ethernet = ethernet  # Use direct attribute setting
            instance.basic_header = basic_header  # Use direct attribute setting
            instance.common_header = common_header  # Use direct attribute setting
            instance.extended_header = extended  # Use direct attribute setting
            instance.btp = btp  # Use direct attribute setting
            instance.its = its

            return instance
        except :
            print("Can't decode the packet")
            return cls()

    def encode(self):
        try :
            if self.secured_header != None:
                assert self.basic_header.data['versionAndNextHeader']['nextHeader'] == 2
                return self.ethernet.encode() + self.basic_header.encode() + self.secured_header.encode()
            return self.ethernet.encode() + self.basic_header.encode() + self.common_header.encode() + self.extended_header.encode() + self.btp.encode() + self.its.encode()
        except :
            print("Can't encode the packet")
            return
    @property
    def data(self):
        return ({
            'ethernet': self.ethernet.data,
            'basicHeader': self.basic_header.data,
            'securedHeader': self.secured_header.data,
            'commonHeader': self.common_header.data,
            'extendedHeader': self.extended_header.data,
            'btp': self.btp.data,
            'its': self.its.data
        })



