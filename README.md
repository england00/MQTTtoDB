# MQTT to DB

This project is a simple implementation of a MQTT client, which receives telemetry and control 
information from the resources of different remote pick and place systems, passing through a 
remote broker. The client is linked to a local MySQL database, which stores all the resources 
of the systems.

The implementation is based on the following Python Frameworks
- Paho: https://pypi.org/project/paho-mqtt/

The client connects to the remote broker with the following parameters (/config/file/mqtt_configuration_client.yaml):
- client_id: "MySQL_DB_consumer"
- broker_ip: "155.185.4.4"
- broker_port: 7883
- account_topic_prefix: "/iot/user/unimore-fum-lab/edge/systems"
- username: "unimore-fum-lab"
- password: "wxugudolcbjttoke"

The local database is linked with the following parameters (/config/file/database.yaml):
- host: "localhost"
- user: "MQTT_client"
- password: "HakertzDB64!"
- charset: "utf8"
- chosen_database: "api_database"

There are also other two configuration file:
- /config/file/systems.yaml, giving the right configuration when database is built and also to setting the systems managing data structure, the system mapper;
- /config/file/resources.yaml, giving the right configuration when database is built and also to setting the resources managing data structure, the resource mapper.

## Modeled Resources

The resources off all the systems are available at the following topics:
- Start Stop Cycle (account_topic_prefix + "/+/" + "production/cycle/signals/start_stop_cycle/control");
- Done Bags (account_topic_prefix + "/+/" + "production/cycle/signals/done_bags/telemetry");
- Total Bags (account_topic_prefix + "/+/" + "production/cycle/signals/total_bags/control");
- Placed Object (account_topic_prefix + "/+/" + "production/cycle/signals/placed_objects/telemetry");
- Cycle Time (account_topic_prefix + "/+/" + "production/cycle/time/telemetry");
- Current Object (account_topic_prefix + "/+/" + "production/cycle/signals/current_object/telemetry");
- Selected Recipes (account_topic_prefix + "/+/" + "production/cycle/recipes/selected_recipe/control");
- Recipe Objects Types (account_topic_prefix + "/+/" + "production/cycle/recipes/objects_types/control");
- Recipe End Effector Indexes (account_topic_prefix + "/+/" + "production/cycle/recipes/end_effector_indexes/control");
- Recipe Object Types Box Positions (account_topic_prefix + "/+/" + "production/cycle/recipes/object_types_box_positions/control");
- Recipe Object Types Numbers (account_topic_prefix + "/+/" + "production/cycle/recipes/object_types_numbers/control");
- Cobot State Cycle (account_topic_prefix + "/+/" + "cobot/states/cobot_state_cycle/telemetry");
- Robot Mode (account_topic_prefix + "/+/" + "cobot/states/robot_mode/telemetry");
- Power On Robot (account_topic_prefix + "/+/" + "cobot/states/power_on_robot/telemetry");
- Safety (account_topic_prefix + "/+/" + "cobot/states/safety/telemetry");
- Joint Angles (account_topic_prefix + "/+/" + "cobot/joints/sensors/angles/telemetry");
- Joint Angles Velocities (account_topic_prefix + "/+/" + "cobot/joints/sensors/velocities/telemetry");
- Joint Current Consumption (account_topic_prefix + "/+/" + "cobot/joints/sensors/current_consumptions/telemetry");
- Joint Temperatures (account_topic_prefix + "/+/" + "cobot/joints/sensors/temperatures/telemetry");
- TCP (account_topic_prefix + "/+/" + "cobot/states/tcp/telemetry");
- 6D Pose Estimation (account_topic_prefix + "/+/" +  "ai_on_edge/inference/6d_pose_estimation/control/response");
- Confidence (account_topic_prefix + "/+/" + "ai_on_edge/inference/scores/confidence/telemetry");
- Cosine Similarity (account_topic_prefix + "/+/" + "ai_on_edge/inference/scores/cosine_similarity/telemetry");
- Inference Time (account_topic_prefix + "/+/" + "ai_on_edge/inference/time/telemetry").

For each resource are available the following attributes:
- uuid (Identifier);
- version;
- name;
- unit;
- topic;
- qos;
- retained;
- frequency;
- value;
- picking_system.