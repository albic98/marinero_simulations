#usr/env/bin python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
# from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    use_4wis4wid = LaunchConfiguration('use_4wis4wid')
    world = LaunchConfiguration('world')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    yaw_pose = LaunchConfiguration('yaw_pose')

    pkg_name='marinero_simulations'

    rviz2_base = os.path.join(get_package_share_directory(pkg_name), 'config')
    rviz2_full_config = os.path.join(rviz2_base, 'marinero_rviz.rviz')
    gazebo_params_file = os.path.join(get_package_share_directory(pkg_name),'config','gazebo_params.yaml')

    world_arg = DeclareLaunchArgument(
        'world',
        # default_value=os.path.join(get_package_share_directory(pkg_name),'worlds','marina_zona_A.world'),
        # default_value=os.path.join(get_package_share_directory(pkg_name),'worlds','marina_zona_B.world'),
        # default_value=os.path.join(get_package_share_directory(pkg_name),'worlds','marina_zona_C.world'),
        default_value=os.path.join(get_package_share_directory(pkg_name),'worlds','marina_zona_A_B_C.world'),
        # default_value=os.path.join(get_package_share_directory(pkg_name),'worlds','marina_base.world'),
        description='Full path to new world.'
    )

    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use sim time if true'
    )

    use_4wis4wid_arg = DeclareLaunchArgument(
        'use_4wis4wid',
        default_value='true',
        description='Choose between Skid Steer or 4WIS4WID controller.'
    )

    ros2_control_arg = DeclareLaunchArgument(
        'use_ros2_control',
        default_value='true',
        description='Choose between gazebo control or ros2 control.'
    )

    x_pose_arg = DeclareLaunchArgument(
        'x_pose',
        default_value='97.2', # '105.0', # '-98'
        description='Define x coordinate when spawning marinero robot'
    )

    y_pose_arg = DeclareLaunchArgument(
        'y_pose',
        default_value='285.8', # '175.0', # '-44'
        description='Define y coordinate when spawning marinero robot'
    )

    direction_arg = DeclareLaunchArgument(
        'yaw_pose',
        default_value="-3.085", # 1.66
        description='Direction in which the robot will be oriented'
    )

    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory('gazebo_ros'),'launch','gazebo.launch.py')
            ]
        ),
        launch_arguments={
            'world': world,
            'extra_gazebo_args': f'--ros-args --params_file{gazebo_params_file}',
        }.items(),
    )

    launch_robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory(pkg_name),'launch','robot_state_publisher.launch.py')
            ]
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'use_ros2_control': use_ros2_control,
            'use_4wis4wid': use_4wis4wid
            }.items()
    )

    world_odom_trans_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments="--x 0 --y 0 --z 0 --roll 0 --pitch 0 --yaw 0 --frame-id world --child-frame-id odom".split(' '),
    )

    world_map_trans_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments="--x 0 --y 0 --z 1.1 --roll 0 --pitch 0 --yaw 0 --frame-id world --child-frame-id map".split(' '),
    )

    spawner_node = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "marinero",
            "-x", x_pose,
            "-y", y_pose,
            "-z", "1.275",
            "-R", "0.0",
            "-P", "0.0",
            "-Y", yaw_pose
        ],
        output= "screen"
    )

    launch_controller_manager = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory(pkg_name),'launch','controllers.launch.py')
            ]
        ),
        condition=IfCondition(use_ros2_control)
    )

    # joy_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         os.path.join(get_package_share_directory(pkg_name),'launch','joystick.launch.py')
    #     ]),
    #     condition=UnlessCondition(use_ros2_control)
    # )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        condition=IfCondition(use_ros2_control)
    )

    marina_marker_node = Node(
        package='marinero_simulations',
        executable='segmented_sdf2marker.py',
    )

    pointcloud_node = Node(
        package='marinero_pointclouds',
        executable='remapped_segmented_pcd_publisher_thread',
    )

    odometry_node = Node(
        package='marinero_control',
        executable='marinero_odometry',
        condition=IfCondition(use_ros2_control)
    )

    control_node = Node(
        package='marinero_control',
        executable='marinero_control',
        remappings=[('/fcc/cmd_vel','/cmd_vel_joy')],
        condition=IfCondition(use_ros2_control)
    )

    marinero_yolo_node = Node(
        package='marinero_control',
        executable='marinero_yolo',
    )

    tracker_node = Node(
        package='marinero_control',
        executable='marinero_tracker',
    )
    
    gazebo_marker_node = Node(
        package='marinero_control',
        executable='gazebo_marker',
    )   

    rviz2_node = Node(
        executable='rviz2',
        output='log',
        arguments=['-d', rviz2_full_config],
    )

    delayed_controller_manager = TimerAction(
        period = 5.0,
        actions = [launch_controller_manager]
    )

    delayed_nodes = TimerAction(
        period = 15.0,
        actions = [tracker_node, marina_marker_node, gazebo_marker_node ,pointcloud_node, marinero_yolo_node]
    )

    return LaunchDescription([
        world_arg,
        x_pose_arg,
        y_pose_arg,
        direction_arg,
        sim_time_arg,
        ros2_control_arg,
        use_4wis4wid_arg,
        world_odom_trans_publisher,
        world_map_trans_publisher,
        launch_robot_state_publisher,
        launch_gazebo,
        spawner_node,
        joy_node,
        control_node,
        odometry_node,
        delayed_controller_manager,
        delayed_nodes,
        rviz2_node,
    ])

## ros2 topic pub -1 /set_joint_trajectory trajectory_msgs/msg/JointTrajectory '{header: {frame_id: base_link},
# joint_names: [camera_base_joint, left_camera_joint, right_camera_joint], points: [{ positions: {0, 1.5, -2.5}}]}'