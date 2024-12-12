#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # joy_params = os.path.join(get_package_share_directory('marinero_simulations'),'config','joystick.yaml')
    # twist_mux_params = os.path.join(get_package_share_directory('marinero_simulations'),'config','twist_mux.yaml')

    joy_node = Node(
        package='joy',
        executable='joy_node',
    )

    odometry_node = Node(
        package='marinero_control',
        executable='marinero_odometry',
    )

    control_node = Node(
        package='marinero_control',
        executable='marinero_control',
        remappings=[('/fcc/cmd_vel','/cmd_vel_joy')],
    )

    # twist_mux_node = Node(
    #     package='twist_mux',
    #     executable='twist_mux',
    #     parameters=[twist_mux_params],
    #     remappings=[('/cmd_vel_out','/cmd_vel')],
    # )

    return LaunchDescription([
        joy_node,
        odometry_node,
        control_node
    ])