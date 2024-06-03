class Ethernet:
    def __init__(self, macDestination, macSource):
        self.name = 'ethernet'
        self.macDestination = macDestination
        self.macSource = macSource
        self.protocol = "8947"

    def encode(self):
        return bytearray.fromhex(self.macDestination + self.macSource + self.protocol)

    @property
    def data(self):
        return {
            'source' : self.macSource,
            'destination' : self.macDestination,
            'protocol' : self.protocol
        }

    @classmethod
    def decode(cls, data):
        # Assuming the MAC addresses are always 12 hex characters each
        macDestination = data[:6].hex()
        macSource = data[6:12].hex()
        protocol = data[12:].hex()

        if protocol != "8947":
            raise ValueError("Invalid protocol type")

        return cls(macDestination, macSource)
