import logging
import yaml
from error.configuration_file_error import ConfigurationFileError
from database.queries.resource_queries import *


class ResourcesMapper:
    _STR_RESOURCE_CONFIG_FILE = "./config/file/resources.yaml"

    def __init__(self, config_object=None, config_file_path=None, base_topic=None, system_id=None, database=None):
        self._resources = {}
        self.myDB = database

        if config_object is not None:
            self._mapper = config_object
        elif config_file_path is not None:
            try:
                with open(config_file_path, 'r') as file:
                    self._mapper = yaml.safe_load(file)
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("Error while reading configuration file") from None
        else:
            try:
                with open(self._STR_RESOURCE_CONFIG_FILE, 'r') as file:
                    self._mapper = yaml.safe_load(file)
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("Error while reading configuration") from None

        try:
            for key in self._mapper["resources"]:
                self._resources[key] = ResourceModel.object_mapping(self._mapper["resources"][key])
                if base_topic is not None:
                    self._resources[key].set_topic(base_topic + self._resources[key].get_topic())
                self._resources[key].set_picking_system(system_id)
        except Exception as e:
            logging.error(str(e))
            raise ConfigurationFileError("Error while parsing configuration data") from None

    def get_resources(self):
        return self._resources

    def add_resource(self, new_resource):
        if isinstance(new_resource, ResourceModel):
            # self.myDB.execute_query(insert_row_resource_table(new_resource, new_resource.get_picking_system()))
            self._resources[new_resource.get_uuid()] = new_resource
        else:
            raise TypeError("Error adding new resource. Only ResourceModel objects are allowed")

    def update_resource(self, update_resource):
        if isinstance(update_resource, ResourceModel):
            self.myDB.execute_query(modify_row_resource_table(update_resource))
            self._resources[update_resource.get_uuid()] = update_resource
        else:
            raise TypeError("Error updating the resource. Only ResourceModel objects are allowed")

    def remove_resource(self, key):
        if key in self._resources.keys():
            # self.myDB.execute_query(delete_row_resource_table(self._resources[key]))
            del self._resources[key]
