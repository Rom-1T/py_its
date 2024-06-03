import os
import random
import time
import asn1tools

from encoder.encoding import cam_foo, denm_foo, ivim_foo
from utils.timestamp import calculate_tst_tai, calculate_timestamp_its

DELTA_TIMESTAMP_ITS_MS_STACK: int = 1072915200000

event_dictionary = {
    1: [0, 1, 2, 3, 4, 5, 6, 7, 8],
    2: 0,
    3: [0, 1, 2, 3, 4, 5, 6],
    6: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    14: [0, 1, 2],
    15: 0,
    17: 0,
    18: 0,
    19: 0,
    26: 0,
    27: 0,
    91: [0, 1, 2, 3, 4, 5, 6, 7, 8],
    92: [0, 1, 2, 3, 4],
    93: [0, 1, 2],
    94: [0, 1, 2, 3, 4, 5],
    95: [0, 1, 2],
    96: [0, 1, 2, 3, 4, 5],
    97: [0, 1, 2, 3, 4],
    99: [0, 1, 2, 3, 4, 5, 6, 7]
}


def generate_random_event():
    # Randomly select a cause code
    cause_code = random.choice(list(event_dictionary.keys()))

    # If sub-cause codes exist for the selected cause code, randomly select one
    sub_cause_code = 0
    sub_cause_codes = event_dictionary[cause_code]
    if sub_cause_codes != 0:
        sub_cause_code = random.choice(sub_cause_codes)

    return cause_code, sub_cause_code

from encoder.encoding import cam_foo, denm_foo, ivim_foo


class ITS:
    def __init__(self):
        self.data = {}

    def set_data(self, data):
        self.data = data

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.set_data(data)
        return instance


class CAM(ITS):
    def __init__(self):
        super().__init__()
        self.data = {
            'header': {
                'protocolVersion': 2,
                'messageID': 2,
                'stationID': 0
            },
            'cam': {
                'generationDeltaTime': 0,
                'camParameters': {
                    'basicContainer': {
                        'stationType': 0,
                        'referencePosition': {
                            'latitude': 900000001,
                            'longitude': 1800000001,
                            'positionConfidenceEllipse': {
                                'semiMajorConfidence': 4095,
                                'semiMinorConfidence': 4095,
                                'semiMajorOrientation': 3601
                            },
                            'altitude': {
                                'altitudeValue': 800001,
                                'altitudeConfidence': 'unavailable'
                            }
                        }
                    },
                    'highFrequencyContainer': ('rsuContainerHighFrequency', {})
                }
            }
        }

    @classmethod
    def from_encoded(cls, encoded_message):
        decoded_cam = cam_foo.decode('CAM', data=encoded_message)
        return cls.from_dict(decoded_cam)

    def encode(self):
        self.bytes = cam_foo.encode('CAM', self.data)
        return self.bytes

    def get_name(self):
        return 'CAM'

    def get_psid(self):
        return 36

    def update_timestamp(self):
        pass





class DENM(ITS):
    def __init__(self):
        super().__init__()
        self.data = {
            'header': {
                'protocolVersion': 2,
                'messageID': 1,
                'stationID': 0
            },
            'denm': {
                'management': {
                    'actionID': {
                        'originatingStationID': 0,
                        'sequenceNumber': 0
                    },
                    'detectionTime': 0,
                    'referenceTime': 0,
                    'eventPosition': {
                        'latitude': 900000001,
                        'longitude': 1800000001,
                        'positionConfidenceEllipse': {
                            'semiMajorConfidence': 4095,
                            'semiMinorConfidence': 4095,
                            'semiMajorOrientation': 3601
                        },
                        'altitude': {
                            'altitudeValue': 800001,
                            'altitudeConfidence': 'unavailable'
                        }
                    },
                    'validityDuration': 600,
                    'stationType': 0
                }
            }
        }

    @classmethod
    def from_encoded(cls, encoded_message):
        decoded_denm = denm_foo.decode('DENM', data=encoded_message)
        return cls.from_dict(decoded_denm)

    def encode(self):
        self.bytes = denm_foo.encode('DENM', self.data)
        return self.bytes

    def get_name(self):
        return 'DENM'

    def get_psid(self):
        return 37

    def update_timestamp(self):
        timestamp = calculate_timestamp_its()
        self.data["denm"]["management"]["detectionTime"] = timestamp
        self.data["denm"]["management"]["referenceTime"] = timestamp



class IVIM(ITS):
    def __init__(self):
        super().__init__()
        self.data = {
            'header': {
                'protocolVersion': 2,
                'messageID': 6,
                'stationID': 0
            },
            'ivi': {
                'mandatory': {
                    'serviceProviderId': {
                        "countryCode": (b'\x00\x00', 10),
                        "providerIdentifier": 0
                    },
                    'iviIdentificationNumber': 1,
                    'iviStatus': 0
                }
            }
        }

    @classmethod
    def from_encoded(cls, encoded_message):
        decoded_ivim = ivim_foo.decode('IVIM', data=encoded_message)
        return cls.from_dict(decoded_ivim)

    def encode(self):
        self.bytes = ivim_foo.encode('IVIM', self.data)
        return self.bytes

    def get_name(self):
        return 'IVIM'

    def get_psid(self):
        return 139

    def update_timestamp(self):
        timestamp = calculate_timestamp_its()
        self.data["ivi"]["mandatory"]["timeStamp"] = timestamp
        previous_validity_duration = self.data["ivi"]["mandatory"]["validTo"] - self.data["ivi"]["mandatory"]["validFrom"]
        self.data["ivi"]["mandatory"]["validFrom"] = timestamp
        self.data["ivi"]["mandatory"]["validTo"] = timestamp + previous_validity_duration

