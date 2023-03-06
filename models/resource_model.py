from interfaces.models.interface_resource_model import IResourceModel
import json


class ResourceModel(IResourceModel):

    def __init__(self, *args):
        self.uuid = None
        self.name = None
        self.version = None
        self.unit = None
        self.topic = None
        self.uri = None
        self.qos = None
        self.retained = None
        self.frequency = None
        self.value = None
        self.picking_system = None

        if len(args) > 0 and isinstance(args[0], dict):
            vars(self).update(args[0])

    def get_uuid(self):
        return self.uuid

    def get_name(self):
        return self.name

    def get_version(self):
        return self.version

    def get_unit(self):
        return self.unit

    def get_topic(self):
        return self.topic

    def get_uri(self):
        return self.uri

    def get_qos(self):
        return self.qos

    def get_retained(self):
        return self.retained

    def get_frequency(self):
        return self.frequency

    def get_value(self):
        return self.value

    def get_picking_system(self):
        return self.picking_system

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_name(self, name):
        self.name = name

    def set_version(self, version):
        self.version = version

    def set_unit(self, unit):
        self.unit = unit

    def set_topic(self, topic):
        self.topic = topic

    def set_uri(self, uri):
        self.uri = uri

    def set_qos(self, qos):
        self.qos = qos

    def set_retained(self, retained):
        self.retained = retained

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_value(self, value):
        self.value = value

    def set_picking_system(self, picking_system):
        self.picking_system = picking_system

    def __str__(self):
        return f'ResourceModel(' \
               f'{self.uuid},' \
               f'{self.name},' \
               f'{self.version},' \
               f'{self.unit},' \
               f'{self.topic},' \
               f'{self.uri},' \
               f'{self.qos},' \
               f'{self.retained},' \
               f'{self.frequency},' \
               f'{self.value},' \
               f'{self.picking_system})'

    @staticmethod
    def object_mapping(dictionary):
        return json.loads(json.dumps(dictionary), object_hook=ResourceModel)
