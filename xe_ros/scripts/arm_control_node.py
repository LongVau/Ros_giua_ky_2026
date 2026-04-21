#!/usr/bin/env python3
import sys
import select
import termios
import tty
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

# Bảng hướng dẫn sử dụng
msg = """
========================================
 ĐIỀU KHIỂN TAY MÁY BẰNG BÀN PHÍM
========================================
Sử dụng các phím sau để điều khiển:

       W : Gập tay máy LÊN (arm_joint +)
 A : Xoay TRÁI        D : Xoay PHẢI (bot_rotate)
       S : Gập tay máy XUỐNG (arm_joint -)

 Nhấn 'Q' hoặc Ctrl+C để thoát.
========================================
"""

def get_key(settings):
    """Hàm đọc phím bấm từ Terminal mà không cần nhấn Enter"""
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class KeyboardArmController(Node):
    def __init__(self):
        super().__init__('keyboard_arm_controller')
        self.publisher_ = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        
        # Góc bắt đầu
        self.bot_rotate_pos = 0.0
        self.arm_joint_pos = 0.0
        
        # Độ lớn của mỗi bước di chuyển (radian)
        self.step_size = 0.1 

    def publish_position(self):
        traj_msg = JointTrajectory()
        traj_msg.joint_names = ['bot_rotate', 'arm_joint']
        
        point = JointTrajectoryPoint()
        point.positions = [self.bot_rotate_pos, self.arm_joint_pos]
        
        # Thời gian thực thi chuyển động (0.2s để phản hồi phím nhanh)
        point.time_from_start = Duration(sec=0, nanosec=200000000) 
        
        traj_msg.points = [point]
        self.publisher_.publish(traj_msg)

def main(args=None):
    # Lưu lại cài đặt terminal hiện tại
    settings = termios.tcgetattr(sys.stdin)
    
    rclpy.init(args=args)
    node = KeyboardArmController()
    
    print(msg)
    
    try:
        while rclpy.ok():
            key = get_key(settings)
            
            # Xử lý logic phím bấm
            if key == 's' or key == 'S':
                node.arm_joint_pos += node.step_size
            elif key == 'w' or key == 'W':
                node.arm_joint_pos -= node.step_size
            elif key == 'a' or key == 'A':
                node.bot_rotate_pos += node.step_size
            elif key == 'd' or key == 'D':
                node.bot_rotate_pos -= node.step_size
            elif key == 'q' or key == 'Q' or key == '\x03': # \x03 là Ctrl+C
                break
            else:
                continue # Nếu bấm phím khác thì bỏ qua

            # Gửi tọa độ mới
            node.publish_position()
            
            # In trạng thái ra màn hình (ghi đè lên dòng hiện tại)
            sys.stdout.write(f"\r[Trạng thái] bot_rotate: {node.bot_rotate_pos:+.2f} rad | arm_joint: {node.arm_joint_pos:+.2f} rad  ")
            sys.stdout.flush()

    except Exception as e:
        print(e)
    finally:
        # Khôi phục lại terminal như cũ
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()
        print("\nĐã thoát điều khiển.")

if __name__ == '__main__':
    main()