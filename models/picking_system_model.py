from interfaces.models.interface_picking_system_model import IPickingSystemModel
import json


class PickingSystemModel(IPickingSystemModel):

    def __init__(self, pick_and_place_id, endpoint, resource_mapper):
        self.pick_and_place_id = pick_and_place_id
        self.endpoint = endpoint
        self.resources_mapper = resource_mapper

    def get_pick_and_place_id(self):
        return self.pick_and_place_id

    def get_endpoint(self):
        return self.endpoint

    def get_resource_mapper(self):
        return self.resources_mapper

    def set_pick_and_place_id(self, pick_and_place_id):
        self.pick_and_place_id = pick_and_place_id

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def set_resource_mapper(self, resource_mapper):
        self.resources_mapper = resource_mapper

    def __str__(self):
        return f'PickingSystemModel(' \
               f'{self.pick_and_place_id},' \
               f'{self.endpoint},' \
               f'{self.resources_mapper})'

    @staticmethod
    def object_mapping(dictionary):
        return json.loads(json.dumps(dictionary), object_hook=PickingSystemModel)
