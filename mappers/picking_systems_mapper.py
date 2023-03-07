from database.queries.picking_system_queries import *
from mappers.resources_mapper import ResourcesMapper


class PickingSystemsMapper:

    def __init__(self, database, mapper):
        self.picking_system_dictionary = {}
        self.myDB = database
        self.mapper = mapper
        self.read_from_yaml()

    def read_from_yaml(self):
        for key in self.mapper["systems"]:
            picking_system_model = PickingSystemModel(pick_and_place_id=self.mapper["systems"][key]["pick_and_place_id"],
                                                      endpoint=self.mapper["systems"][key]["endpoint"],
                                                      resource_mapper=ResourcesMapper(system_id=self.mapper["systems"][key]["pick_and_place_id"]))
            self.picking_system_dictionary[picking_system_model.pick_and_place_id] = picking_system_model

    def get_systems(self):
        return self.picking_system_dictionary

    def add_system(self, newPickingSystem):
        if isinstance(newPickingSystem, PickingSystemModel):  # check data type
            if newPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                raise TypeError("ERROR adding new system! This ID already exists!")
            else:
                self.myDB.execute_query(insert_row_picking_system_table(newPickingSystem))
                self.picking_system_dictionary[newPickingSystem.pick_and_place_id] = newPickingSystem
        else:
            raise TypeError("ERROR adding new device! Only PickingSystemModel are allowed!")

    def update_system(self, updatedPickingSystem):
        if isinstance(updatedPickingSystem, PickingSystemModel):  # check data type
            if updatedPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                self.myDB.execute_query(modify_row_picking_system_table(updatedPickingSystem))
                self.picking_system_dictionary[updatedPickingSystem.pick_and_place_id] = updatedPickingSystem
            else:
                raise TypeError("ERROR updating the system! This ID doesn't exists!")
        else:
            raise TypeError("ERROR updating the device! Only PickingSystemModel are allowed!")

    def remove_system(self, pick_and_place_id):
        if pick_and_place_id in self.picking_system_dictionary.keys():
            if pick_and_place_id in self.picking_system_dictionary.keys():
                self.myDB.execute_query(delete_row_picking_system_table(self.picking_system_dictionary[pick_and_place_id]))
                del self.picking_system_dictionary[pick_and_place_id]
            else:
                raise TypeError("ERROR deleting the system! This ID doesn't exists!")
