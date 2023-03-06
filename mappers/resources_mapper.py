import logging
import yaml
from database.queries.resource_queries import *
from models.resource_model import ResourceModel
from error.configuration_file_error import ConfigurationFileError


class ResourcesMapper:
    _STR_RESOURCE_CONFIG_FILE = "./config/resources.yaml"

    def __init__(self, config_object=None, config_file_path=None, base_topic=None, initialization=False, system_id=None, database=None):
        self._resources = {}
        self.myDB = database

        if not initialization and system_id is None:

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
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("Error while parsing configuration data") from None

        else:

            for resource in self.myDB.read_query(showing_resource_table_join_system("*", system_id)):
                resource_model = ResourceModel()
                resource_model.set_uuid(str(resource[0]))
                resource_model.set_name((str(str(resource[1]).replace("[", "")).replace("]", ""))
                                        .replace(" ", "").split(','))
                resource_model.set_version(float(resource[2]))
                resource_model.set_unit((str(str(resource[3]).replace("[", "")).replace("]", ""))
                                        .replace(" ", "").split(','))
                resource_model.set_topic(str(resource[4]))
                resource_model.set_uri(str(resource[5]))
                resource_model.set_qos(int(resource[6]))
                resource_model.set_retained(bool(resource[7]))
                resource_model.set_frequency(int(resource[8]))
                resource_model.set_value((str(str(resource[9]).replace("[", "")).replace("]", ""))
                                         .replace(" ", "").split(','))
                resource_model.set_picking_system(str(resource[10]))
                self._resources[resource_model.uuid] = resource_model

    def get_resource(self, key):
        return self._resources[key]

    def get_resources(self):
        return self._resources

    def set_resources(self, resources):
        self._resources = resources

    def add_resource(self, new_resource):
        if isinstance(new_resource, ResourceModel):
            # self.myDB.execute_query(insert_row_resource_table(new_resource, new_resource.get_picking_system()))
            self._resources[new_resource.get_uuid()] = new_resource
        else:
            raise TypeError("Error adding new resource. Only ResourceModel objects are allowed")

    def update_resource(self, update_resource):
        if isinstance(update_resource, ResourceModel):
            # self.myDB.execute_query(modify_row_resource_table(update_resource))
            self._resources[update_resource.get_uuid()] = update_resource
        else:
            raise TypeError("Error updating the resource. Only ResourceModel objects are allowed")

    def remove_resource(self, key):
        if key in self._resources.keys():
            # self.myDB.execute_query(delete_row_resource_table(self._resources[key]))
            del self._resources[key]
