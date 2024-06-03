from encoder.encoding import geonet_foo
from utils.timestamp import calculate_tst_tai


class GeonetPacket:
    def __init__(self, packet_type):
        self.packet_type = packet_type
        self.data = {}

    def __repr__(self):
        return f'{self.packet_type}({self.data})'

    @classmethod
    def from_dict(cls, data_dict):
        raise NotImplementedError("This method should be implemented in subclasses.")


class BasicHeader(GeonetPacket):
    def __init__(self, protocol_version, next_header, lifetime_base, life_time_multp, remain_hope_limit):
        super().__init__('BasicHeader')
        self.data = {
            'versionAndNextHeader': {'version': protocol_version, 'nextHeader': next_header},
            'reserved': 0,
            'lifeTime': {
                'multiplier': life_time_multp,
                'base': lifetime_base
            },
            'remainHopeLimit': remain_hope_limit
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['versionAndNextHeader']['version'],
                   data_dict['versionAndNextHeader']['nextHeader'],
                   data_dict['lifeTime']['base'],
                   data_dict['lifeTime']['multiplier'],
                   data_dict['remainHopeLimit'])

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("BasicHeader", data)
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("BasicHeader", self.data)


class CommonHeader(GeonetPacket):
    def __init__(self, payload_next_header, traffic_class_id, payload_length, maximum_hope_limit, ):
        super().__init__('CommonHeader')
        self.data = {
            'nextHeader': 2,
            'reserved1': 0,
            'headerType': {
                'type': payload_next_header[0],
                'subType': payload_next_header[1]
            },
            'trafficClass': {
                'scf': False,
                'channelOffload': False,
                'id': traffic_class_id
            },
            'flags': {
                'itsGnIsMobile': True,
                'reserved': 0
            },
            'payloadLength': payload_length,
            'maximumHopLimit': maximum_hope_limit,
            'reserved2': 0
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls((data_dict['headerType']['type'], data_dict['headerType']['subType']),
                   data_dict['trafficClass']['id'],
                   data_dict['payloadLength'],
                   data_dict['maximumHopLimit'])

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("CommonHeader", data)
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("CommonHeader", self.data)

    def update_size(self, new_size):
        self.data["payloadLength"] = new_size


class Beacon(GeonetPacket):
    def __init__(self, stationType, manual, llAddr, timeStamp, latitude, longitude, speed, positionAccuracy, heading):
        super().__init__('LongPositionVector')
        self.data = {
            'geonetAddress': {
                'stationType': stationType,
                'manual': manual,
                'reserved1': 0,
                'reserved2': 0,
                'llAddr': llAddr
            },
            'timeStamp': timeStamp,
            'latitude': latitude - 2147483648,
            'longitude': longitude - 2147483648,
            'speed': speed - 16384,
            'positionAccuracy': positionAccuracy,
            'heading': heading
        }
        self.size = 24

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['geonetAddress']['stationType'],
                   data_dict['geonetAddress']['manual'],
                   data_dict['geonetAddress']['llAddr'],
                   data_dict['timeStamp'],
                   data_dict['latitude'] + 2147483648,
                   data_dict['longitude'] + 2147483648,
                   data_dict['speed'] + 16384,
                   data_dict['positionAccuracy'],
                   data_dict['heading'])

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("LongPositionVector", data[:24])
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("LongPositionVector", self.data)

    def update_timestamp(self):
        timestamp = calculate_tst_tai()[1]
        self.data['sourcePosition']["timeStamp"] = timestamp


class TopologicalBroadcast(GeonetPacket):
    def __init__(self, sequence_number, stationType, manual, llAddr, timeStamp, latitude, longitude, speed, positionAccuracy,
                 heading):
        super().__init__('TopologicalBroadcast')
        self.data = {
            'sequenceNumber': sequence_number,
            'reserved': 0,
            'sourcePosition': {
                'geonetAddress': {
                    'stationType': stationType,
                    'manual': manual,
                    'reserved1': 0,
                    'reserved2': 0,
                    'llAddr': llAddr
                },
                'timeStamp': timeStamp,
                'latitude': latitude - 2147483648,
                'longitude': longitude - 2147483648,
                'speed': speed - 16384,
                'positionAccuracy': positionAccuracy,
                'heading': heading
            }
        }
        self.size = 28

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['sequenceNumber'],
                   data_dict['sourcePosition']['geonetAddress']['stationType'],
                   data_dict['sourcePosition']['geonetAddress']['manual'],
                   data_dict['sourcePosition']['geonetAddress']['llAddr'],
                   data_dict['sourcePosition']['timeStamp'],
                   data_dict['sourcePosition']['latitude'] + 2147483648,
                   data_dict['sourcePosition']['longitude'] + 2147483648,
                   data_dict['sourcePosition']['speed'] + 16384,
                   data_dict['sourcePosition']['positionAccuracy'],
                   data_dict['sourcePosition']['heading'])

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("TopologicalBroadcast", data[:28])
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("TopologicalBroadcast", self.data)

    def update_timestamp(self):
        timestamp = calculate_tst_tai()[1]
        self.data['sourcePosition']["timeStamp"] = timestamp


class GeoUniCast(GeonetPacket):
    def __init__(self, sequenceNumber, stationType, manual, llAddr, timeStamp, latitude, longitude, speed, positionAccuracy,
                 heading,
                 destStationType, destManual, destLlAddr, destTimeStamp, destLatitude, destLongitude):
        super().__init__('GeoUniCast')
        self.data = {
            'sequenceNumber': sequenceNumber,
            'reserved': 0,
            'sourcePosition': {
                'geonetAddress': {
                    'stationType': stationType,
                    'manual': manual,
                    'reserved1': 0,
                    'reserved2': 0,
                    'llAddr': llAddr
                },
                'timeStamp': timeStamp,
                'latitude': latitude - 2147483648,
                'longitude': longitude - 2147483648,
                'speed': speed - 16384,
                'positionAccuracy': positionAccuracy,
                'heading': heading
            },
            'destinationPosition': {
                'geonetAddress': {
                    'stationType': destStationType,
                    'manual': destManual,
                    'reserved1': 0,
                    'reserved2': 0,
                    'llAddr': destLlAddr
                },
                'timeStamp': destTimeStamp,
                'latitude': destLatitude - 2147483648,
                'longitude': destLongitude - 2147483648,
            }
        }
        self.size = 48

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict['data']
        return cls(
            data['sequenceNumber'],
            data['sourcePosition']['geonetAddress']['stationType'],
            data['sourcePosition']['geonetAddress']['manual'],
            data['sourcePosition']['geonetAddress']['llAddr'],
            data['sourcePosition']['timeStamp'],
            data['sourcePosition']['latitude'] + 2147483648,
            data['sourcePosition']['longitude'] + 2147483648,
            data['sourcePosition']['speed'] + 16384,
            data['sourcePosition']['positionAccuracy'],
            data['sourcePosition']['heading'],
            data['destinationPosition']['geonetAddress']['stationType'],
            data['destinationPosition']['geonetAddress']['manual'],
            data['destinationPosition']['geonetAddress']['llAddr'],
            data['destinationPosition']['timeStamp'],
            data['destinationPosition']['latitude'] + 2147483648,
            data['destinationPosition']['longitude'] + 2147483648
        )

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("GeoUniCast", data[:48])
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("GeoUniCast", self.data)

    def update_timestamp(self):
        timestamp = calculate_tst_tai()[1]
        self.data['sourcePosition']["timeStamp"] = timestamp
        self.data['destinationPosition']["timeStamp"] = timestamp


class GeoBroadCast(GeonetPacket):
    def __init__(self, stationType, manual, llAddr, timeStamp, latitude, longitude, speed, positionAccuracy,
                 heading, sequenceNumber=0, geoLatitude=0, geoLongitude=0, aDistance=0, bDistance=0,
                 angle=0):
        super().__init__('GeoBroadCast')
        self.data = {
            'sequenceNumber': sequenceNumber,
            'reserved': 0,
            'sourcePosition': {
                'geonetAddress': {
                    'stationType': stationType,
                    'manual': manual,
                    'reserved1': 0,
                    'reserved2': 0,
                    'llAddr': llAddr
                },
                'timeStamp': timeStamp,
                'latitude': latitude - 2147483648,
                'longitude': longitude - 2147483648,
                'speed': speed - 16384,
                'positionAccuracy': positionAccuracy,
                'heading': heading
            },
            'geoAreaPosLatitude': geoLatitude - 2147483648,
            'geoAreaPosLongitude': geoLongitude - 2147483648,
            'aDistance': aDistance,
            'bDistance': bDistance,
            'angle': angle,
            'reserved2': 0
        }
        self.size = 44

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['sourcePosition']['geonetAddress']['stationType'],
                   data_dict['sourcePosition']['geonetAddress']['manual'],
                   data_dict['sourcePosition']['geonetAddress']['llAddr'],
                   data_dict['sourcePosition']['timeStamp'],
                   data_dict['sourcePosition']['latitude'] + 2147483648,
                   data_dict['sourcePosition']['longitude'] + 2147483648,
                   data_dict['sourcePosition']['speed'] + 16384,
                   data_dict['sourcePosition']['positionAccuracy'],
                   data_dict['sourcePosition']['heading'],
                   data_dict['sequenceNumber'],
                   data_dict['geoAreaPosLatitude'] + 2147483648,
                   data_dict['geoAreaPosLongitude'] + 2147483648,
                   data_dict['aDistance'],
                   data_dict['bDistance'],
                   data_dict['angle'])

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("GeoBroadCast", data[:44])
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("GeoBroadCast", self.data)

    def update_timestamp(self):
        timestamp = calculate_tst_tai()[1]
        self.data['sourcePosition']["timeStamp"] = timestamp


class SingleHopeBroadcast(GeonetPacket):
    def __init__(self, mediaDependentData, stationType, manual, llAddr, timeStamp, latitude, longitude, speed, positionAccuracy,
                 heading):
        super().__init__('SingleHopeBroadcast')
        self.data = {
            'mediaDependentData': mediaDependentData,
            'sourcePosition': {
                'geonetAddress': {
                    'stationType': stationType,
                    'manual': manual,
                    'reserved1': 0,
                    'reserved2': 0,
                    'llAddr': llAddr
                },
                'timeStamp': timeStamp,
                'latitude': latitude - 2147483648,
                'longitude': longitude - 2147483648,
                'speed': speed - 16384,
                'positionAccuracy': positionAccuracy,
                'heading': heading
            }
        }
        self.size = 28

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['mediaDependentData'],
                   data_dict['sourcePosition']['geonetAddress']['stationType'],
                   data_dict['sourcePosition']['geonetAddress']['manual'],
                   data_dict['sourcePosition']['geonetAddress']['llAddr'],
                   data_dict['sourcePosition']['timeStamp'],
                   data_dict['sourcePosition']['latitude'] + 2147483648,
                   data_dict['sourcePosition']['longitude'] + 2147483648,
                   data_dict['sourcePosition']['speed'] + 16384,
                   data_dict['sourcePosition']['positionAccuracy'],
                   data_dict['sourcePosition']['heading'])

    @classmethod
    def from_encoded(cls, data):
        decoded = geonet_foo.decode("SingleHopeBroadcast", data[:28])
        return cls.from_dict(decoded)

    def encode(self):
        return geonet_foo.encode("SingleHopeBroadcast", self.data)

    def update_timestamp(self):
        timestamp = calculate_tst_tai()[1]
        self.data['sourcePosition']["timeStamp"] = timestamp
