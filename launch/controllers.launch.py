from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    
    forward_position_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['forward_position_controller']
    )

    forward_velocity_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['forward_velocity_controller']
    )

    joint_trajectory_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller']
    )
    
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster']
    )
    # start_controllers = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=joint_state_broadcaster,
    #         on_exit=[forward_velocity_controller,
    #                  forward_position_controller])
    # )
    
    return LaunchDescription([
        joint_state_broadcaster,
        forward_position_controller,
        forward_velocity_controller,
        # joint_trajectory_controller,
    ])