# tf_publisher.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # base_link -> sensor_kit_base_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'sensor_kit_base_link']
        ),
        # sensor_kit_base_link -> velodyne_top_base_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0.89', '-0.175', '0.4785', '0.795398', '0', '0', 'sensor_kit_base_link', 'velodyne_top_base_link']
        ),
        # sensor_kit_base_link -> velodyne_rear_base_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['-0.14004940104906838', '-0.18298809976550123', '0.4785', '-0.7824923633571231', '0.003576648236547806', '0.0016378038700001624', 'sensor_kit_base_link', 'velodyne_rear_base_link']
        ),
        # velodyne_top_base_link -> velodyne_top
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0.072', '0', '0', '0', 'velodyne_top_base_link', 'velodyne_top']
        ),
        # velodyne_rear_base_link -> velodyne_rear
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0.072', '0', '0', '0', 'velodyne_rear_base_link', 'velodyne_rear']
        ),
    ])