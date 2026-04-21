cmake_minimum_required(VERSION 3.8)
project(xe_ros)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Tìm hệ thống build của ROS 2
find_package(ament_cmake REQUIRED)

# Install các thư mục chứa file mô hình, config và launch
# ROS 2 yêu cầu các file này nằm trong thư mục share của package
install(
  DIRECTORY config launch meshes urdf rviz
  DESTINATION share/${PROJECT_NAME}
)

# Lệnh bắt buộc ở cuối mỗi file CMakeLists.txt của ROS 2
ament_package()