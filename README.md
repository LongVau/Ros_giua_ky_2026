## Giới thiệu
Mô phỏng hoạt động của một robot chạy bằng cơ cấu Ackermann (car-like), với 3 sensor (LiDAR, Camera, GPS), và một tay máy 2 link, 2 khớp xoay 
* **Cơ cấu di chuyển:** Sử dụng plugin gazebo_ros_ackermann_drive để điều khiển xe mượt mà
* **Manipulator:** Cánh tay 2 bậc tự do (Pan-Tilt) được điều khiển vị trí mượt mà thông qua hệ sinh thái `ros2_control` và `joint_trajectory_controller`.
* **Sensors:** Tích hợp và hiển thị đồng bộ trên RViz hoặc trên terminal:
  * Lidar
  * Camera
  * GPS (hiển thị tọa độ của robot trên terminal)

## Chạy

### Dọn dẹp và Build Workspace
```bash
cd ~/humble_ws #(Có thể đổi tên workspace khác nếu cần thiết)
# Dọn rác (optional)
rm -rf build/ install/ log/

# Build package, tạo môi trường làm việc
colcon build
source install/setup.bash
```

### Khởi động môi trường (Terminal 1)

```bash
# Trường hợp Gazebo không thể tìm thấy file mesh (.STL), ta phải chỉ đường cho nó
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/humble_ws/install/xe_ros/share # Có thể thay đổi đường dẫn thành đường dẫn tới vị trí tương ứng trong máy khác

# Khởi động Gazebo và RViz
ros2 launch xe_ros gazebo.launch.py
```

### Di chuyển Robot (Terminal 2)
Sử dụng gói Teleop mặc định của ROS 2 để phát vào topic `cmd_vel`:

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Hướng dẫn sẽ hiện ra trên màn hình terminal

### Điều khiển Tay máy
Điều khiển tay máy trực tiếp trên terminal để đơn giản hóa package
```bash
ros2 topic pub /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: ['bot_rotate', 'arm_joint'],
  points: [{
    positions: [0.5, 0.5], # Có thể thay đối giá trị ở đây, với bot_rotate là continous, arm_joint có limit từ -0.6 đến 0.6
    time_from_start: {sec: 2, nanosec: 0}
  }]
}" -1
```

### Hiện tọa độ của xe bằng GPS
Ngoại trừ GPS, tất cả những sensor khác sẽ được hiển thị trong RViz, vì thế nên chúng ta có thể nhìn vào topic /gps để có thể xác định được tọa độ của xe
```bash
ros2 topic echo /gps/fix
```

