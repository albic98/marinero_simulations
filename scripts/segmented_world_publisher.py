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



class WorldPublisher(Node):

    def __init__(self):
        super().__init__("sdf_2_marker_publisher")

        self.zone_A = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/world_zona_A/model.sdf",
            "euler_angles": [0.0, 0.0, 0.0],
            "translation": [-100.0, -48.0, 0.08],
        }
        self.zone_B = {
            "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/world_zona_B/model.sdf",
            "euler_angles": [0.0, 0.0, 0.0],
            "translation": [93.64, 305.75, 0.08],
        }
        # self.zone_C = {
        #     "sdf_file_path": "/home/albert/marinero_ws/src/marinero_simulations/models/Marina_Zona_C/model.sdf",
        #     "euler_angles": [0.0, 0.0, 0.0],
        #     "translation": [140.85, 598.8, 0.08],
        # }
    


def main(args=None):
    
    rclpy.init(args=args)
    converter = WorldPublisher()
    rclpy.spin(converter)
    converter.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()