import paho.mqtt.client as mqtt
from interfaces.mqtt.subscriber.interface_mqtt_subscriber_client import IMqttSubscriberClient
from utils.senml.senml_pack import SenMLPack
from utils.format.jsonsenml.format_json_senml import FormatJsonSenML


class MqttSubscriberClient(IMqttSubscriberClient):
    def __init__(self, mqtt_client_configuration, system_mapper):
        self.client_id = mqtt_client_configuration["client_id"]
        self.broker_ip_address = mqtt_client_configuration["broker_ip"]
        self.broker_port = mqtt_client_configuration["broker_port"]
        self.interval_s = mqtt_client_configuration["interval_s"]
        self.timeout_s = mqtt_client_configuration["timeout_s"]
        self.username = mqtt_client_configuration["username"]
        self.password = mqtt_client_configuration["password"]
        self.base_topic = mqtt_client_configuration["account_topic_prefix"]
        self.system_mapper = system_mapper
        self.topic_dictionary = self.obtaining_topic_list()
        self.mqtt_subscriber_client = None
        self.initialize()

    def obtaining_topic_list(self):
        topic_dictionary = {}
        for system in self.system_mapper.get_systems().values():
            topic_dictionary[system.get_pick_and_place_id()] = []
            for resource in system.get_resource_mapper().get_resources().values():
                topic_dictionary[resource.get_picking_system()].append(resource.get_topic())
        return topic_dictionary

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
        for system in self.topic_dictionary.keys():
            for resource_topic in self.topic_dictionary[system]:
                self.mqtt_subscriber_client.subscribe("{}/{}/{}".format(self.base_topic, system, resource_topic))
                print("Subscribed to: " + self.base_topic + "/" + system + "/" + resource_topic)

    def on_message(self, client, userdata, message):
        for system in self.system_mapper.get_systems().values():
            if mqtt.topic_matches_sub(self.base_topic,
                                      str(message.topic).split("/{}".format(system.get_pick_and_place_id()))[0]):
                for resource in system.get_resource_mapper().get_resources().values():
                    if mqtt.topic_matches_sub(self.base_topic + "/" + str(system.get_pick_and_place_id()),
                                              str(message.topic).split("/{}".format(resource.get_topic()))[0]):
                        message_payload = str(message.payload.decode("utf-8"))
                        senMLPack = SenMLPack()
                        senMLPack.from_json(message_payload)
                        form = FormatJsonSenML()
                        resource.set_qos(message.qos)
                        resource.set_retained(message.retain)
                        form.from_format(senMLPack, resource)
                        system.get_resource_mapper().update_resource(resource)
                        print(message.topic)

    def connect(self):
        self.mqtt_subscriber_client.connect(self.broker_ip_address, self.broker_port)

    def start_forever(self):
        self.mqtt_subscriber_client.loop_forever()
