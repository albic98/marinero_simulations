#!/usr/bin/env python3

import os

import rclpy
import math
from rclpy.node import Node
import xml.etree.ElementTree as ET
import tf_transformations as tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from rclpy.parameter import Parameter
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from visualization_msgs.msg import Marker, MarkerArray
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster



class SDF2Marker(Node):

    def __init__(self):
        super().__init__("sdf_2_marker_publisher")

        self.zone_A = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/Marina_Zona_A/model.sdf",
            "euler_angles": [0.0, 0.0, 0.0],
            "translation": [-100.0, -48.0, 0.08],
        }
        self.zone_B = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/Marina_Zona_B/model.sdf",
            "euler_angles": [0.0, 0.0, 0.0],
            "translation": [93.35, 305.75, 0.08],
        }
        # self.zone_C = {
        #     "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/Marina_Zona_C/model.sdf",
        #     "euler_angles": [0.0, 0.0, 0.0],
        #     "translation": [140.85, 598.8, 0.08],
        # }
        
        self.current_zone = None
        self.sdf_published = False

        self.sdf_publisher = self.create_publisher(MarkerArray, "/sdf_markers", 10)
        self.pose_subsriber = self.create_subscription(Odometry, "/marinero/odom", self.odom_callback, 50)
        self.counter = 0       
        self.br = TransformBroadcaster(self)
        self.tf_broad = StaticTransformBroadcaster(self)

    def publish_marker(self, file_path):
            # Read SDF file
            with open(file_path, "r") as file:
                sdf_xml_string = file.read()

            # Publish SDF as Marker Array
            self.marker_array = self.create_marker_array_from_sdf(sdf_xml_string)

            self.static_transform_publisher()
            self.sdf_publisher.publish(self.marker_array)
        
    def odom_callback(self, msg):
        self.pose_x = msg.pose.pose.position.x
        self.pose_y = msg.pose.pose.position.y
        
        if 250.0 <= self.pose_y < 296.0 and -100.0 < self.pose_x < -95.0:
            if self.current_zone == self.zone_B:
                pass
            else:
                self.switch_to_zone(self.zone_B, "Opening zone B.")
                
        elif self.pose_y < 296.0 and self.current_zone != self.zone_A:
            self.switch_to_zone(self.zone_A, "Opening zone A.")
            
        elif 296.5 <= self.pose_y < 598.0 and self.current_zone != self.zone_B:
            self.switch_to_zone(self.zone_B, "Opening zone B.")
            
        elif 598.0 <= self.pose_y < 624.0 and -100.0 < self.pose_x < -95.0:
            if self.current_zone == self.zone_B:
                pass
            else:
                self.switch_to_zone(self.zone_B, "Opening zone B.")
                
        # elif self.pose_y > 598.5 and self.current_zone != self.zone_C:
        #     self.switch_to_zone(self.zone_C, "Opening zone C.")
        
        self.declare_parameter_if_not_declared("sdf_file_path", self.current_zone["sdf_file_path"])
        self.declare_parameter_if_not_declared("euler_angles", self.current_zone["euler_angles"])
        self.declare_parameter_if_not_declared("translation", self.current_zone["translation"])

        self.sdf_file_path = self.get_parameter("sdf_file_path").get_parameter_value().string_value
        self.euler_angles = [angle * math.pi / 180 for angle in self.get_parameter("euler_angles").get_parameter_value().double_array_value]
        self.translation = self.get_parameter("translation").get_parameter_value().double_array_value
        
        if not self.sdf_published:
            self.publish_marker(self.sdf_file_path)
            self.sdf_published = True

    def switch_to_zone(self, new_zone, log_message):
        self.current_zone = new_zone
        self.sdf_published = False
        self.get_logger().info(log_message)
        
    def declare_parameter_if_not_declared(self, param_name, value):
        if not self.has_parameter(param_name):
            self.declare_parameter(param_name, value)
        else:
            self.set_parameters([Parameter(param_name, Parameter.Type.from_parameter_value(value), value)])

    def static_transform_publisher(self):
        rotation_angle = tf.quaternion_from_euler(self.euler_angles[0], self.euler_angles[1], self.euler_angles[2])
        
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"
        t.child_frame_id = "sdf_frame"
        t.transform.translation.x = self.translation[0]
        t.transform.translation.y = self.translation[1]
        t.transform.translation.z = self.translation[2]
        t.transform.rotation.x = rotation_angle[0]
        t.transform.rotation.y = rotation_angle[1]
        t.transform.rotation.z = rotation_angle[2]
        t.transform.rotation.w = rotation_angle[3]
        self.tf_broad.sendTransform(t)

    def create_marker_array_from_sdf(self, sdf_xml_string):
        root = ET.fromstring(sdf_xml_string)

        # Create MarkerArray for visualization
        marker_array = MarkerArray()

        # Parse visual geometry
        visual = root.find(".//visual")
        visual_pose = visual.find("pose").text.split()
        visual_uri = visual.find(".//mesh/uri").text
        visual_scale = visual.find(".//mesh/scale").text.split()

        # Create visual marker
        visual_marker = Marker()
        visual_marker.header.frame_id = "sdf_frame"
        visual_marker.type = Marker.MESH_RESOURCE
        visual_marker.action = Marker.ADD
        visual_marker.pose.position = Point(x=0.0, 
                                            y=0.0, 
                                            z=0.0)
        visual_marker.pose.orientation.w = 1.0
        visual_marker.scale.x = float(visual_scale[0]) 
        visual_marker.scale.y = float(visual_scale[1])
        visual_marker.scale.z = float(visual_scale[2])
        visual_marker.color.r = 0.278
        visual_marker.color.g = 0.129
        visual_marker.color.b = 0.02
        visual_marker.color.a = 0.8
        visual_marker.mesh_resource = "file://" + os.path.abspath(visual_uri)
        visual_marker.mesh_use_embedded_materials = True
        visual_marker.id = 0
        marker_array.markers.append(visual_marker)

        return marker_array


def main(args=None):
    
    rclpy.init(args=args)
    converter = SDF2Marker()
    rclpy.spin(converter)
    converter.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()