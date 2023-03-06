import paho.mqtt.client as mqtt
import json
from interfaces.mqtt.interface_mqtt_publisher_client import IMqttPublisherClient
from config.method.configuration_loader import yaml_loader



class MqttPublisherClient(IMqttPublisherClient):
    def __init__(self, mqtt_client_configuration, STR_MQTT_CONFIG_FILE):
        self.client_id = mqtt_client_configuration.CLIENT_ID
        self.broker_ip_address = mqtt_client_configuration.BROKER_IP_ADDRESS
        self.broker_port = mqtt_client_configuration.BROKER_PORT
        self.timeout_s = mqtt_client_configuration.TIMETOUT_S
        self.username = mqtt_client_configuration.USERNAME
        self.password = mqtt_client_configuration.PASSWORD
        self.base_topic = mqtt_client_configuration.BASE_TOPIC

        self.mqtt_publisher_client = None

        self.initialize()

    def initialize(self):
        self.mqtt_publisher_client = mqtt.Client(self.client_id)
        self.mqtt_publisher_client.on_connect = self.on_connect
        self.mqtt_publisher_client.username_pw_set(self.username, self.password)

    def connect(self):
        self.mqtt_publisher_client.connect(self.broker_ip_address, self.broker_port)

    def start(self):
        self.mqtt_publisher_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        pass

    def publish(self, target_topic, model, qos, retained):
        # json_data = model.to_json()
        json_data = json.dumps(model, default=lambda o: o.__dict__)
        topic = "{}/{}".format(self.base_topic, target_topic)
        self.mqtt_publisher_client.publish(topic, json_data, qos, retained)

    def stop(self):
        self.mqtt_publisher_client.loop_stop()
