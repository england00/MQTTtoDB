import logging
from error.general_error import GeneralError
from models.resource_model import ResourceModel
from models.picking_system_model import PickingSystemModel


def create_resource_table():
    return """
        CREATE TABLE resource (
        uuid VARCHAR(100) NOT NULL,
        name VARCHAR(100),
        version INT,
        unit VARCHAR(100),
        topic VARCHAR(200) NOT NULL,
        uri VARCHAR(200) NOT NULL,
        qos INT, 
        retained VARCHAR(100),
        frequency INT,
        value VARCHAR(100), 
        picking_system VARCHAR(100) NOT NULL,
        PRIMARY KEY (uuid, uri, picking_system));
        """


def relation_resource_and_picking_system_table():
    return """
        ALTER TABLE resource
        ADD FOREIGN KEY(picking_system)
        REFERENCES picking_system(pick_and_place_id);
        """


def showing_resource_table_join_system(column, system_name):
    return """SELECT {} 
              FROM resource
              WHERE picking_system = '{}'
           """.format(str(column), str(system_name))


def insert_row_resource_table(resource, system):
    try:
        if isinstance(resource, ResourceModel):
            if isinstance(system, PickingSystemModel):
                return """
                    INSERT INTO resource (uuid, name, version, unit, topic, uri, qos, retained, frequency, value, 
                    picking_system) 
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
                    """.format(str(resource.get_uuid()), str(resource.get_name()).replace("'", ""),
                               resource.get_version(),
                               str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                               str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                               resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                               str(system.get_pick_and_place_id()))
            else:
                return """
                    INSERT INTO resource (uuid, name, version, unit, topic, uri, qos, retained, frequency, value, 
                    picking_system) 
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                    """.format(str(resource.get_uuid()), str(resource.get_name()).replace("'", ""),
                               resource.get_version(),
                               str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                               str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                               resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                               str(resource.get_picking_system()))
    except Exception as e:
        logging.error(str(e))
        raise GeneralError("ERROR: problem occurred while adding new resource. "
                           "Only ResourceModel objects are allowed") from None


def modify_row_resource_table(resource):
    try:
        if isinstance(resource, ResourceModel):
            return """
                UPDATE resource
                SET name = '{}', version = '{}', unit = '{}', topic = '{}', uri = '{}', qos = '{}', retained = '{}', 
                frequency = '{}', value = '{}'
                WHERE (uuid = '{}' AND picking_system = '{}');
                """.format(str(resource.get_name()).replace("'", ""), resource.get_version(),
                           str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                           str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                           resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                           str(resource.get_uuid()), str(resource.get_picking_system()))
    except Exception as e:
        logging.error(str(e))
        raise GeneralError("ERROR: problem occurred while updating the resource. "
                           "Only ResourceModel objects are allowed") from None


def delete_row_resource_table(resource):
    try:
        if isinstance(resource, ResourceModel):
            return """
                DELETE
                FROM resource
                WHERE (uuid = '{}' AND picking_system = '{}')
                """.format(str(resource.get_uuid()), str(resource.get_picking_system()))
    except Exception as e:
        logging.error(str(e))
        raise GeneralError("ERROR: problem occurred while deleting the resource. "
                           "Only ResourceModel objects are allowed") from None


def delete_resource_table():
    return """
        DROP TABLE resource
        """


def check_resource(column, uri, endpoint):
    return """SELECT {}
              FROM resource
              WHERE (uri = '{}' AND picking_system = '{}')
              """.format(str(column), str(uri), str(endpoint))


def from_db_row_to_object(resource):
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
    if resource[7] == "True":
        resource_model.set_retained(True)
    else:
        resource_model.set_retained(False)
    resource_model.set_frequency(int(resource[8]))
    resource_model.set_value((str(str(resource[9]).replace("[", "")).replace("]", ""))
                             .replace(" ", "").split(','))
    resource_model.set_picking_system(str(resource[10]))
    return resource_model
