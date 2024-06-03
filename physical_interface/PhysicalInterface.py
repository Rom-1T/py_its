from socket import *
# import paho.mqtt.client as mqtt

class PhysicalInterface:
    def __init__(self):
        self.socket = socket(AF_PACKET, SOCK_RAW)
        try:
            self.socket.bind(('lo', 0))
        except:
            self.socket.bind(('lo', 0))

    def send(self, message):
        return self.socket.send(message)

class MqttInterface :
    def __init__(self, broker_address: str, broker_port: int, topic_out:str, topic_in:str):
        self.brokerAddress = broker_address
        self.brokerPort = broker_port
        self.topic_out = topic_out
        self.topic_in = topic_in

        self.mqttClient = mqtt.Client()

        # Set callbacks
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_publish = self.on_publish
        self.mqttClient.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic_in)

    def on_publish(self, client, userdata, mid):
        print("Message published")
        pass

    def on_message(self, client, userdata, msg):
        print("Message received from topic : ", msg.topic)
        print("Payload : ", msg.payload)

    def publish_message(self, msg, msgType = 'CAM'):
        self.mqttClient.publish(self.topic_out + msgType, msg)


class UdpInterface:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def send(self, message):
        self.socket.sendto(message, (self.ip_address, self.port))

    def close(self):
        self.socket.close()