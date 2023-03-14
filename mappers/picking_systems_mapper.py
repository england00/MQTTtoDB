import yaml
from database.queries.picking_system_queries import *
from mappers.resources_mapper import ResourcesMapper
from error.configuration_file_error import ConfigurationFileError
from error.general_error import GeneralError


class PickingSystemsMapper:

    def __init__(self, database=None, config_file_path=None, config_resource_file_path=None):
        self.picking_system_dictionary = {}
        self.myDB = database

        if config_file_path is not None and config_resource_file_path is not None:
            try:
                with open(config_file_path, 'r') as file:
                    self._mapper = yaml.safe_load(file)
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("ERROR: problem occurred while reading configuration") from None

            try:
                for key in self._mapper["systems"]:
                    value = self._mapper["systems"][key]
                    self.picking_system_dictionary[key] = PickingSystemModel(value['pick_and_place_id'],
                                                                             value['endpoint'],
                                                                             ResourcesMapper(
                                                                                 config_file_path=config_resource_file_path))
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("ERROR: problem occurred while parsing configuration data") from None

        else:
            self.read_from_db()

    def read_from_db(self):
        for system in self.myDB.read_query(showing_picking_system_table()):
            picking_system_model = PickingSystemModel(str(system[0]), str(system[1]), ResourcesMapper(initialization=True, system_id=system[0], database=self.myDB))
            self.picking_system_dictionary[picking_system_model.pick_and_place_id] = picking_system_model

    def get_systems(self):
        if self.myDB is not None:
            self.read_from_db()
            return self.picking_system_dictionary
        else:
            return self.picking_system_dictionary

    def add_system(self, newPickingSystem):
        if isinstance(newPickingSystem, PickingSystemModel):  # check data type
            if newPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                raise GeneralError("ERROR: problem occurred while adding new system. "
                                   "This ID already exists") from None
            else:
                self.myDB.execute_query(insert_row_picking_system_table(newPickingSystem))
                self.picking_system_dictionary[newPickingSystem.pick_and_place_id] = newPickingSystem
        else:
            raise GeneralError("ERROR: problem occurred while adding new system. "
                               "Only PickingSystemModel are allowed") from None

    def update_system(self, updatedPickingSystem):
        if isinstance(updatedPickingSystem, PickingSystemModel):  # check data type
            if updatedPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                self.myDB.execute_query(modify_row_picking_system_table(updatedPickingSystem))
                self.picking_system_dictionary[updatedPickingSystem.pick_and_place_id] = updatedPickingSystem
            else:
                raise GeneralError("ERROR: problem occurred while updating the system. "
                                   "This ID doesn't exists") from None
        else:
            raise GeneralError("ERROR: problem occurred while updating the system. "
                               "Only PickingSystemModel are allowed") from None

    def remove_system(self, pick_and_place_id):
        if pick_and_place_id in self.picking_system_dictionary.keys():
            if pick_and_place_id in self.picking_system_dictionary.keys():
                self.myDB.execute_query(
                    delete_row_picking_system_table(self.picking_system_dictionary[pick_and_place_id]))
                del self.picking_system_dictionary[pick_and_place_id]
            else:
                raise GeneralError("ERROR: problem occurred while deleting the system. "
                                   "This ID doesn't exists") from None
