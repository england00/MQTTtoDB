from models.picking_system_model import PickingSystemModel


def create_picking_system_table():
    return """
        CREATE TABLE picking_system (
        pick_and_place_id VARCHAR(100) NOT NULL,
        endpoint VARCHAR(100) NOT NULL,
        PRIMARY KEY (pick_and_place_id));
        """


def showing_picking_system_table():
    return """SELECT * 
              FROM picking_system
           """


def insert_row_picking_system_table(picking_system):
    if isinstance(picking_system, PickingSystemModel):
        return """
            INSERT INTO picking_system (pick_and_place_id, endpoint) 
            VALUES ('{}', '{}');
            """.format(str(picking_system.get_pick_and_place_id()), str(picking_system.get_endpoint()))
    else:
        raise TypeError("Error adding new picking_system. Only PickingSystemModel objects are allowed")


def modify_row_picking_system_table(picking_system):
    if isinstance(picking_system, PickingSystemModel):
        return """
            UPDATE picking_system 
            SET endpoint = '{}'
            WHERE (pick_and_place_id = '{}');
            """.format(str(picking_system.get_endpoint()), str(picking_system.get_pick_and_place_id()))
    else:
        raise TypeError("Error adding new picking_system. Only PickingSystemModel objects are allowed")


def delete_row_picking_system_table(picking_system):
    if isinstance(picking_system, PickingSystemModel):
        return """
            DELETE
            FROM picking_system 
            WHERE (pick_and_place_id = '{}');
            """.format(str(picking_system.get_pick_and_place_id()))
    else:
        raise TypeError("Error adding new picking_system. Only PickingSystemModel objects are allowed")


def delete_picking_system_table():
    return """
        DROP TABLE picking_system
        """
