from config.method.configuration_loader import yaml_loader
from database.model.database import MySQLDatabase
from mappers.picking_systems_mapper import PickingSystemsMapper
from mqtt.subscriber.mqtt_subscriber_client import MqttSubscriberClient

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ # CONFIGURATION # ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

STR_DATABASE_CONFIG_FILE = "config/file/database.yaml"
STR_MQTT_CONFIG_FILE = "config/file/mqtt_configuration_client.yaml"
STR_RESOURCES_CONFIG_FILE = "config/file/resources.yaml"
STR_SYSTEMS_CONFIG_FILE = "config/file/systems.yaml"


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MAIN # ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

# executing the code (MQTTs)
if __name__ == '__main__':
    # loading database configuration
    db_params = yaml_loader(STR_DATABASE_CONFIG_FILE)

    # creating a MySQLDatabase object
    myDB = MySQLDatabase(db_params["host"], db_params["user"], db_params["password"], db_params["charset"])

    # opening connection with MySQL and choosing the right database
    myDB.start_connection()
    myDB.choose_database(db_params["chosen_database"])

    # loading systems configuration
    systems_params = yaml_loader(STR_SYSTEMS_CONFIG_FILE)

    # creating an object PickingSystemsMapper
    picking_system_mapper = PickingSystemsMapper(myDB, systems_params)

    # loading mqtt client configuration
    mqtt_params = yaml_loader(STR_MQTT_CONFIG_FILE)

    # creating MqttSubscriberClient object
    sub = MqttSubscriberClient(mqtt_params, picking_system_mapper)

    # opening connection with a broker in cloud
    sub.connect()
    sub.start_forever()

    # closing connection with MySQL
    myDB.close_connection()
