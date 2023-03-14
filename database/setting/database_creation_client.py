from config.method.configuration_loader import yaml_loader
from database.model.database import MySQLDatabase
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *
from mappers.picking_systems_mapper import PickingSystemsMapper

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ # CONFIGURATION # ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

STR_DATABASE_CONFIG_FILE = "../../config/file/database.yaml"
STR_RESOURCE_CONFIG_FILE = "../../config/file/resources.yaml"
STR_SYSTEMS_CONFIG_FILE = "../../config/file/systems.yaml"

# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MAIN # ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    # LOADING DATABASE CONFIGURATION
    db_params = yaml_loader(STR_DATABASE_CONFIG_FILE)

    # CREATING A MySQLDatabase OBJECT
    myDB = MySQLDatabase(db_params["host"], db_params["user"], db_params["password"], db_params["charset"])

    # STARTING CONNECTION
    myDB.start_connection()

    # DATABASE CREATION
    myDB.create_database(db_params["chosen_database"])

    # CHOOSING DATABASE
    myDB.choose_database(db_params["chosen_database"])

    # TABLE CREATION
    myDB.execute_query(create_picking_system_table())
    myDB.execute_query(create_resource_table())
    myDB.execute_query(relation_resource_and_picking_system_table())

    # CREATING AN OBJECT PickingSystemsMapper
    picking_system_mapper = PickingSystemsMapper(config_file_path=STR_SYSTEMS_CONFIG_FILE,
                                                 config_resource_file_path=STR_RESOURCE_CONFIG_FILE)

    # INSERTING ROWS IN PICKING SYSTEM TABLE AND IN RESOURCE TABLE
    for system in picking_system_mapper.get_systems().values():
        # adding a system
        myDB.execute_query(insert_row_picking_system_table(system))
        # adding the resources for this system
        for resource in system.get_resource_mapper().get_resources().values():
            myDB.execute_query(insert_row_resource_table(resource, system))

    # CLOSING CONNECTION
    myDB.close_connection()
