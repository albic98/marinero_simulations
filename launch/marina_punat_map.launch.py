#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node, LoadComposableNodes
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, TimerAction

def generate_launch_description():

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': '/home/albert/marinero_ws/src/marinero_simulations/config/marina_punat_map/marina_punat.yaml'}],
    )

    return LaunchDescription([
        map_server_node
    ])