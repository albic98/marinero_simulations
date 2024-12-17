#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown

def generate_launch_description():

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': '/home/albert/marinero_ws/src/marinero_simulations/config/marina_punat_map/marina_punat.yaml'}],
    )

    configure_map_server = ExecuteProcess(
        cmd=['ros2', 'lifecycle', 'set', '/map_server', 'configure'],
        output='screen'
    )

    activate_map_server = ExecuteProcess(
        cmd=['ros2', 'lifecycle', 'set', '/map_server', 'activate'],
        output='screen'
    )

    shutdown_map_server = ExecuteProcess(
        cmd=['ros2', 'lifecycle', 'set', '/map_server', 'shutdown'],
        output='screen'
    )

    delayed_configure = TimerAction(
        period=2.0,
        actions=[configure_map_server]
    )

    delayed_activate = TimerAction(
        period=4.0,
        actions=[activate_map_server]
    )

    on_shutdown_handler = RegisterEventHandler(
        OnProcessExit(
            target_action=map_server_node,
            on_exit=[shutdown_map_server]
        )
    )

    return LaunchDescription([
        map_server_node,
        delayed_configure,
        delayed_activate,
        on_shutdown_handler
    ])