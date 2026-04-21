import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_xe_ros = get_package_share_directory('xe_ros')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # 1. Khởi động Gazebo World
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Node Static Transform
    tf_footprint_base = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'base_link', '--child-frame-id', 'base_footprint'
        ]
    )

    # Đọc nội dung file URDF
    urdf_file_path = os.path.join(pkg_xe_ros, 'urdf', 'xe_ros.urdf')
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()
    rviz_config_path = os.path.join(pkg_xe_ros, 'rviz', 'xe_ros.rviz')
    # 3. Node Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True # Khuyến khích bật khi chạy mô phỏng
        }]
    )

    # 4. Spawn mô hình vào Gazebo
    spawn_model = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_model',
        output='screen',
        arguments=['-entity', 'xe_ros', '-topic', 'robot_description']
    )

    # 5. Kích hoạt Controller Manager và nạp các controller
    
    # Nạp bộ công bố trạng thái khớp
    load_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    # Nạp bộ điều khiển cánh tay 
    # (Chỉ cần gọi tên controller, file YAML đã được nạp qua thẻ <parameters> trong URDF)
    load_arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
    )
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        tf_footprint_base,
        node_robot_state_publisher,
        spawn_model,
        load_joint_state_broadcaster,
        load_arm_controller,
        rviz2
    ])