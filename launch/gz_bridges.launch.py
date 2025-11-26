#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_name='marinero_simulations'
    bridge_params = os.path.join(get_package_share_directory(pkg_name),'config','gz_bridge.yaml')    

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}']
    )

    gz_bridge_image_node = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/right_depth_camera', '/right_depth_camera/image_raw'],
        output='screen'
    )

    return LaunchDescription([
    gz_bridge_node,
    gz_bridge_image_node,
    ])

