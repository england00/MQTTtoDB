import paho.mqtt.client as mqtt
import json
from interfaces.mqtt.subscriber.interface_mqtt_subscriber_client import IMqttSubscriberClient


class MqttSubscriberClient(IMqttSubscriberClient):
    def __init__(self, mqtt_client_configuration):
        self.client_id = mqtt_client_configuration["client_id"]
        self.broker_ip_address = mqtt_client_configuration["broker_ip"]
        self.broker_port = mqtt_client_configuration["broker_port"]
        self.interval_s = mqtt_client_configuration["interval_s"]
        self.timeout_s = mqtt_client_configuration["timeout_s"]
        self.username = mqtt_client_configuration["username"]
        self.password = mqtt_client_configuration["password"]
        self.base_topic = mqtt_client_configuration["account_topic_prefix"]
        self.topic_list = mqtt_client_configuration["topic_list"]
        self.mqtt_subscriber_client = None
        self.initialize()

    def initialize(self):
        self.mqtt_subscriber_client = mqtt.Client(client_id=self.client_id,
                                                  clean_session=True,
                                                  userdata=None,
                                                  protocol=mqtt.MQTTv311,
                                                  transport="tcp")
        self.mqtt_subscriber_client.on_message = self.on_message
        self.mqtt_subscriber_client.on_connect = self.on_connect
        self.mqtt_subscriber_client.username_pw_set(self.username, self.password)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {}".format(rc))
        for resource_topic in self.topic_list:
            self.mqtt_subscriber_client.subscribe("{}/+/{}".format(self.base_topic, resource_topic))
            print("Subscribed to: " + self.base_topic + "/+/" + resource_topic)

    def on_message(self, client, userdata, message):
        for resource_topic in self.topic_list:
            if mqtt.topic_matches_sub(self.base_topic + "/+/" + resource_topic, message.topic):
                message_payload = str(message.payload.decode("utf-8"))
                print(message.topic, message_payload)
        else:
            print("Unmanaged Topic !")

    def connect(self):
        self.mqtt_subscriber_client.connect(self.broker_ip_address, self.broker_port)

    def start_forever(self):
        self.mqtt_subscriber_client.loop_forever()
