#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    joy_params = os.path.join(get_package_share_directory('marinero_simulations'),'config','skid_steer_joystick.yaml')
    twist_mux_params = os.path.join(get_package_share_directory('marinero_simulations'),'config','twist_mux.yaml')

    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use sim time if true.'
    )
    
    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[joy_params, {'use_sim_time': use_sim_time}] 
    ) 

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_node',
        parameters=[joy_params, {'use_sim_time': use_sim_time}]
    )

    camera_node = Node(
        package='marinero_control',
        executable='marinero_camera_w_joy',
    )

    twist_mux_node = Node(
        package='twist_mux',
        executable='twist_mux',
        parameters=[twist_mux_params],
        remappings=[('/cmd_vel_out','/cmd_vel_joy')],
    )

    twist_stamper_node = Node(
        package='twist_stamper',
        executable='twist_stamper',
        parameters=[{'use_sim_time': use_sim_time}],
        remappings=[('/cmd_vel_in', '/cmd_vel'),
                    ('/cmd_vel_out', '/cmd_vel_stamped')]
    )

    return LaunchDescription([
        sim_time_arg,
        joy_node,
        teleop_node,
        camera_node,
        twist_stamper_node,
        # twist_mux_node,
        
    ])