#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from geometry_msgs.msg import PoseStamped
from gazebo_msgs.srv import SpawnEntity, DeleteEntity

class WorldSpawner(Node):

    def __init__(self, x_pose, y_pose):
        super().__init__("gazebo_world_spawner")

        self.zone_A = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_A_environment/model.sdf",
            "translation": [0.0, 0.0, 0.0], # [-100.225, -48.3232, 0.0],
            "sdf_objects": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_A_objects/model.sdf",
            "translation_objects": [0.0, 0.0, 0.0],
        }
        self.zone_B = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_B_environment/model.sdf",
            "translation": [0.0, 0.0, 0.0], # [94.3188, 292.84, 0.0],
            "sdf_objects": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_B_objects/model.sdf",
            "translation_objects": [0.0, 0.0, 0.0],
        }
        self.zone_C = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_C_environment/model.sdf",
            "translation": [0.0, 0.0, 0.0], # [140.34, 587.60, 0.0],
            "sdf_objects": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_C_objects/model.sdf",
            "translation_objects": [0.0, 0.0, 0.0],
        }
        
        self.pose_subscriber = self.create_subscription(PoseStamped, "/robot_pose", self.pose_callback, 10)
        self.spawn_client = self.create_client(SpawnEntity, "/spawn_entity")
        self.delete_client = self.create_client(DeleteEntity, "/delete_entity")

        self.spawn_client.wait_for_service(timeout_sec=1.0)
        self.delete_client.wait_for_service(timeout_sec=1.0)

        self.labels = ["A", "B", "C"]
        self.spawn_label = None
        self.delete_label = None
        self.current_zone = None
        self.previous_zone = None
        self.current_objects = None
        self.previous_objects = None
        self.zone_spawned = False
        self.zone_deleted = False
        self.objects_spawned = False
        self.objects_deleted = False

        self.initialize_zones(y_pose)

    def initialize_zones(self, y_pose):
        if y_pose < 296.0:
            self.spawn_zone(self.zone_A, self.labels[0])
            self.spawn_objects(self.zone_A, self.labels[0])
        elif 296.0 <= y_pose < 598.0:
            self.spawn_zone(self.zone_B, self.labels[1])
            self.spawn_objects(self.zone_B, self.labels[1])
        else:
            self.spawn_zone(self.zone_C, self.labels[2])
            self.spawn_objects(self.zone_C, self.labels[2])

    def pose_callback(self, msg):
        self.pose_x = msg.pose.position.x
        self.pose_y = msg.pose.position.y

        zone_A_limit_1, zone_A_limit_2 = 250.0, 296.0
        zone_B_limit_1, zone_B_limit_2, zone_B_limit_3 = 296.5, 598.0, 624.0
        zone_C_limit = 598.5
        zone_x_min, zone_x_max = -100.0, -95.0     
        x_pose_condition = zone_x_min < self.pose_x < zone_x_max

        if zone_A_limit_1 <= self.pose_y < zone_A_limit_2 and x_pose_condition:
            if self.current_zone != self.zone_B:
                self.spawn_zone(self.zone_B, self.labels[1])
                self.delete_zone(self.previous_zone)
                self.spawn_objects(self.zone_B, self.labels[1])
                self.delete_objects(self.previous_objects)
        elif self.pose_y < zone_A_limit_2 and self.current_zone != self.zone_A:
            self.spawn_zone(self.zone_A, self.labels[0])
            self.delete_zone(self.previous_zone)
            self.spawn_objects(self.zone_A, self.labels[0])
            self.delete_objects(self.previous_objects)
        elif zone_B_limit_1 <= self.pose_y < zone_B_limit_2 and self.current_zone != self.zone_B:
            self.spawn_zone(self.zone_B, self.labels[1])
            self.delete_zone(self.previous_zone)
            self.spawn_objects(self.zone_B, self.labels[1])
            self.delete_objects(self.previous_objects)
        elif zone_B_limit_2 <= self.pose_y < zone_B_limit_3 and x_pose_condition:
            if self.current_zone != self.zone_B:
                self.spawn_zone(self.zone_B, self.labels[1])
                self.delete_zone(self.previous_zone)
                self.spawn_objects(self.zone_B, self.labels[1])
                self.delete_objects(self.previous_objects)
        elif self.pose_y > zone_C_limit and self.current_zone != self.zone_C:
            self.spawn_zone(self.zone_C, self.labels[2])
            self.delete_zone(self.previous_zone)
            self.spawn_objects(self.zone_C, self.labels[2])
            self.delete_objects(self.previous_objects)
        self.previous_zone = self.current_zone
        self.previous_objects = self.current_objects

    def declare_parameter_if_not_declared(self, param_name, value):
        if not self.has_parameter(param_name):
            self.declare_parameter(param_name, value)
        else:
            self.set_parameters([Parameter(param_name, Parameter.Type.from_parameter_value(value), value)])


    def spawn_zone(self, new_zone, spawn_label):

        self.current_zone = new_zone
        self.spawn_label = spawn_label
        self.declare_parameter_if_not_declared("sdf_file_path", self.current_zone["sdf_file_path"])
        self.declare_parameter_if_not_declared("translation", self.current_zone["translation"])
        self.sdf_file_path = self.get_parameter("sdf_file_path").get_parameter_value().string_value
        self.translation = self.get_parameter("translation").get_parameter_value().double_array_value

        self.zone_deleted = False

        if self.zone_spawned:
            return

        with open(self.sdf_file_path, "r") as f:
            self.sdf_content = f.read()

        zone_request = SpawnEntity.Request()
        zone_request.name = f"zone_{self.spawn_label}"
        zone_request.xml = self.sdf_content
        zone_request.initial_pose.position.x = self.translation[0]
        zone_request.initial_pose.position.y = self.translation[1]
        zone_request.initial_pose.position.z = self.translation[2]
        future = self.spawn_client.call_async(zone_request)
        future.add_done_callback(self.spawn_zone_response_callback)

    def spawn_zone_response_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                self.get_logger().info(f"Zone {self.spawn_label} spawned successfully!")
                self.zone_spawned = False
                self.zone_deleted = False
        except Exception as e:
            self.get_logger().error(f"Service call failed: {str(e)}")


    def spawn_objects(self, new_objects, spawn_label):

        self.current_objects = new_objects
        self.spawn_label = spawn_label
        
        self.declare_parameter_if_not_declared("sdf_objects", self.current_objects["sdf_objects"])
        self.declare_parameter_if_not_declared("translation_objects", self.current_objects["translation_objects"])
        self.sdf_objects = self.get_parameter("sdf_objects").get_parameter_value().string_value
        self.translation = self.get_parameter("translation_objects").get_parameter_value().double_array_value

        self.objects_deleted = False

        if self.objects_spawned:
            return

        with open(self.sdf_objects, "r") as f:
            self.sdf_content = f.read()

        zone_request = SpawnEntity.Request()
        zone_request.name = f"objects_zone_{self.spawn_label}"
        zone_request.xml = self.sdf_content
        zone_request.initial_pose.position.x = self.translation[0]
        zone_request.initial_pose.position.y = self.translation[1]
        zone_request.initial_pose.position.z = self.translation[2]
        future = self.spawn_client.call_async(zone_request)
        future.add_done_callback(self.spawn_objects_response_callback)

    def spawn_objects_response_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                # self.get_logger().info(f"Objects from zone {self.spawn_label} spawned successfully!")
                self.objects_spawned = False
                self.objects_deleted = False
        except Exception as e:
            self.get_logger().error(f"Service call failed: {str(e)}")


    def delete_zone(self, previous_zone):

        if previous_zone is None:
            # self.get_logger().info("No zone to delete.")
            return

        if not self.zone_deleted:
            if previous_zone == self.zone_A:
                self.delete_label = self.labels[0]
            elif previous_zone == self.zone_B:
                self.delete_label = self.labels[1]
            elif previous_zone == self.zone_C:
                self.delete_label = self.labels[2]
            else:
                self.get_logger().error("Unknown zone.")
                return

            zone_delete = DeleteEntity.Request()
            zone_delete.name = f"zone_{self.delete_label}"
            future = self.delete_client.call_async(zone_delete)
            future.add_done_callback(self.delete_zone_response_callback)

    def delete_zone_response_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                # self.get_logger().info(f"Zone {self.delete_label} deleted successfully!")
                self.zone_spawned = False
                self.zone_deleted = True
        except Exception as e:
            self.get_logger().error(f"Service call failed: {str(e)}")


    def delete_objects(self, previous_objects):

        if previous_objects is None:
            # self.get_logger().info("No objects to delete.")
            return

        if not self.objects_deleted:
            if previous_objects == self.zone_A:
                self.delete_label = self.labels[0]
            elif previous_objects == self.zone_B:
                self.delete_label = self.labels[1]
            elif previous_objects == self.zone_C:
                self.delete_label = self.labels[2]
            else:
                self.get_logger().error("Unknown objects.")
                return

            zone_delete = DeleteEntity.Request()
            zone_delete.name = f"objects_zone_{self.delete_label}"
            future = self.delete_client.call_async(zone_delete)
            future.add_done_callback(self.delete_objects_response_callback)

    def delete_objects_response_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                # self.get_logger().info(f"Objects from zone {self.delete_label} deleted successfully!")
                self.objects_spawned = False
                self.objects_deleted = True
        except Exception as e:
            self.get_logger().error(f"Service call failed: {str(e)}")

def main(args=None):
    
    rclpy.init(args=args)
    
    if len(sys.argv) < 3:
        print("Usage: ros2 run marinero_simulations segmented_world_publisher.py <x_pose> <y_pose>")
        sys.exit(1)
        
    x_pose = float(sys.argv[1])
    y_pose = float(sys.argv[2])

    world_spawner = WorldSpawner(x_pose, y_pose)

    rclpy.spin(world_spawner)
    world_spawner.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()