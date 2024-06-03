btp_port = {
    # https://www.etsi.org/deliver/etsi_ts/103200_103299/103248/02.03.01_60/ts_103248v020301p.pdf
    'CAM': 2001,
    'DENM': 2002,
    'MAPEM': 2003,
    'SPATEM': 2004,
    'SAEM': 2005,
    'IVIM': 2006,
    'SREM': 2007,
    'SSEM': 2008,
    'CPM': 2009,
    'POI': 2010,
    'TRM': 2011,
    'EV-RSR': 2012,
    'RTCMEM': 2013,
    'CTLM': 2014,
    'CRLM': 2015,
    'EC': 2016,
    'MCDM': 2017,
    'VAM': 2018,
    'DSM': 2019
}

# Reverse the btp_port dictionary to interpret ports
btp_port_reverse = {v: k for k, v in btp_port.items()}


class BTP:
    def __init__(self, destination_port, destination_port_info):
        self.destination_port = destination_port
        self.destination_port_info = destination_port_info

    def encode(self):
        dest_port_bytes = self.destination_port.to_bytes(2, byteorder='big')
        dest_port_info_bytes = self.destination_port_info.to_bytes(2, byteorder='big')
        return dest_port_bytes + dest_port_info_bytes

    @classmethod
    def decode(cls, encoded_data):
        if len(encoded_data) != 4:
            raise ValueError("Invalid BTP packet length")

        destination_port = int.from_bytes(encoded_data[:2], byteorder='big')
        destination_port_info = int.from_bytes(encoded_data[2:4], byteorder='big')

        return cls(destination_port, destination_port_info)

    @classmethod
    def from_message_type(cls, its_message_type):
        if its_message_type not in btp_port:
            raise ValueError("Invalid ITS message type")

        destination_port = btp_port[its_message_type]
        destination_port_info = 0000  # Default value or modify as needed

        return cls(destination_port, destination_port_info)

    @property
    def data(self):
        return ({
            'destinationPort': self.destination_port,
            'destinationPortInfo': self.destination_port_info
        })

    def interpret_port(self):
        return btp_port_reverse.get(self.destination_port, "Unknown Port")

# Example usage
# encoded_btp = bytearray.fromhex("07d20000")
# print("Encoded BTP:", encoded_btp.hex())
#
# decoded_btp = BTP.decode(encoded_btp)
# print("Decoded BTP:", decoded_btp.destination_port, decoded_btp.destination_port_info)
# print("Interpreted Port:", decoded_btp.interpret_port())
