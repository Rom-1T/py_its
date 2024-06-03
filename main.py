from ITS.its import CAM, DENM, IVIM
from ITS.geonet.geonet_layer import BasicHeader, CommonHeader, GeoBroadCast
from ITS.packet import ItsMessage
from physical_interface.PhysicalInterface import PhysicalInterface
import time
from ITS.ethernet import Ethernet
from security.security_layer import SecurityLayer, SecuredPacket
from ITS.btp import BTP


TEST_SECURITY = False

# # UTILISATION :
interface = PhysicalInterface()
security_lay = SecurityLayer()

packet = ItsMessage()

packet.ethernet = Ethernet("ffffffffffff", "000000011000")
packet.its = CAM()
packet.btp = BTP.from_message_type(packet.its.get_name())
packet.extended_header = GeoBroadCast(stationType=15, llAddr=b'\x00\x00\x00\x00\x00\x00',timeStamp=3939123435, latitude=503180850, longitude=35111685, speed=0, positionAccuracy=True, heading=0,
                              geoLatitude=503180850, geoLongitude=35111685, aDistance=5000, manual = False)
packet.common_header = CommonHeader(payload_next_header=(4,0), traffic_class_id=2, payload_length=len(packet.its.encode() + packet.btp.encode()), maximum_hope_limit=5)

if TEST_SECURITY :
    #Add security :
    packet.secured_header = SecuredPacket.from_encoded(security_lay.sign_its(its_message=packet.its, common_header_gnw=packet.common_header, btp_packet=packet.btp.encode(), payload_gnw=packet.extended_header))
    packet.basic_header = BasicHeader(protocol_version=1, next_header=2, lifetime_base=5, life_time_multp=5, remain_hope_limit=1)
else :
    packet.basic_header = BasicHeader(protocol_version=1, next_header=1, lifetime_base=5, life_time_multp=5,
                                      remain_hope_limit=1)
while True:
    interface.send(message=packet.encode())
    time.sleep(0.5)
