#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, LogInfo

def generate_launch_description():

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': '/home/albert/marinero_ws/src/marinero_simulations/config/marina_punat_map/marina_punat.yaml'}],

    )
    local_costmap_node = Node(
        package='nav2_costmap_2d',
        executable='nav2_costmap_2d',
        name='local_costmap',
        output='screen',
        parameters=['/home/albert/marinero_ws/src/marinero_simulations/config/local_costmap_params.yaml'],
    )
    global_costmap_node = Node(
        package='nav2_costmap_2d',
        executable='nav2_costmap_2d',
        name='global_costmap',
        output='screen',
        parameters=['/home/albert/marinero_ws/src/marinero_simulations/config/global_costmap_params.yaml'],
    )

    return LaunchDescription([
        map_server_node,
        global_costmap_node,
        local_costmap_node,
    ])