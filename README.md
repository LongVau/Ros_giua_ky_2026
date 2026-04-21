# Ros_giua_ky_2026
bài ROS giữa kỳ sử dụng cơ cấu lái Avkermann, 3 sensor (LiDAR, GPS, Camera) và 1 tay máy 2 link, 2 khớp xoay

# điều khiển tay máy:
ros2 topic pub /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: ['bot_rotate', 'arm_joint'],
  points: [{
    positions: [0.5, 0.5],
    time_from_start: {sec: 2, nanosec: 0}
  }]
}" -1
có thể thay thông số trong positions
