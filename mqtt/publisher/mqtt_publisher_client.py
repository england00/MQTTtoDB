import paho.mqtt.client as mqtt
import json
from interfaces.mqtt.publisher.interface_mqtt_publisher_client import IMqttPublisherClient


class MqttPublisherClient(IMqttPublisherClient):
    def __init__(self, mqtt_client_configuration):
        self.client_id = "Test_Publisher"
        self.broker_ip_address = mqtt_client_configuration["broker_ip"]
        self.broker_port = mqtt_client_configuration["broker_port"]
        self.interval_s = mqtt_client_configuration["interval_s"]
        self.timeout_s = mqtt_client_configuration["timeout_s"]
        self.username = mqtt_client_configuration["username"]
        self.password = mqtt_client_configuration["password"]
        self.base_topic = mqtt_client_configuration["account_topic_prefix"]
        self.mqtt_publisher_client = None
        self.initialize()

    def initialize(self):
        self.mqtt_publisher_client = mqtt.Client(client_id=self.client_id,
                                                 clean_session=True,
                                                 userdata=None,
                                                 protocol=mqtt.MQTTv311,
                                                 transport="tcp")
        self.mqtt_publisher_client.on_connect = self.on_connect
        self.mqtt_publisher_client.username_pw_set(self.username, self.password)

    def connect(self):
        self.mqtt_publisher_client.connect(self.broker_ip_address, self.broker_port)

    def start(self):
        self.mqtt_publisher_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def publish(self, target_topic, model, qos, retained):
        json_data = json.dumps(model, default=lambda o: o.__dict__)
        topic = "{}/{}".format(self.base_topic, target_topic)
        self.mqtt_publisher_client.publish(topic, json_data, qos, retained)

    def stop(self):
        self.mqtt_publisher_client.loop_stop()
