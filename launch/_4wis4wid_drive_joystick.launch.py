#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    # joy_params = os.path.join(get_package_share_directory('marinero_simulations'),'config','_4wis4wid_drive_joystick.yaml')
    twist_mux_params = os.path.join(get_package_share_directory('marinero_simulations'),'config','twist_mux_4wis4wid.yaml')

    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use sim time if true.'
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    odometry_node = Node(
        package='marinero_control',
        executable='marinero_odometry',
    )

    teleop_node = Node(
        package='marinero_control',
        executable='marinero_teleop',
    )

    control_node = Node(
        package='marinero_control',
        executable='marinero_control_with_autonomy',
    )

    twist_mux_node = Node(
        package='twist_mux',
        executable='twist_mux',
        parameters=[twist_mux_params]
    )

    twist_stamper_node = Node(
        package='twist_stamper',
        executable='twist_stamper',
        remappings=[('/cmd_vel_in', '/cmd_vel_joy'),
                    ('/cmd_vel_out', '/cmd_vel_stamped')]
    )

    return LaunchDescription([
        sim_time_arg,
        joy_node,
        odometry_node,
        teleop_node,
        control_node,
        # twist_mux_node,
        twist_stamper_node
    ])