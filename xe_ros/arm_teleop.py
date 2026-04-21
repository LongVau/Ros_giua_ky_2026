#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys
import termios
import tty

msg = """
Điều khiển Cánh tay Robot bằng Bàn phím!
---------------------------------------
Phím điều khiển:
   W : Gập tay (arm_joint) LÊN
   S : Gập tay (arm_joint) XUỐNG
   
   A : Xoay đế (bot_rotate) TRÁI
   D : Xoay đế (bot_rotate) PHẢI

Space / X : Reset tay về vị trí ban đầu (0, 0)
CTRL-C để thoát
"""

class ArmTeleop(Node):
    def __init__(self):
        super().__init__('arm_teleop_keyboard')
        self.publisher_ = self.create_publisher(Float64MultiArray, '/arm_position_controller/commands', 10)
        
        # Góc quay mặc định ban đầu
        self.bot_angle = 0.0
        self.arm_angle = 0.0
        
        # Độ nhạy (bước nhảy góc mỗi lần bấm phím - radian)
        self.step = 0.1

    def send_angles(self):
        command = Float64MultiArray()
        # [bot_rotate, arm_joint] - phải đúng thứ tự khai báo trong YAML
        command.data = [self.bot_angle, self.arm_angle] 
        self.publisher_.publish(command)

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = ArmTeleop()

    print(msg)

    try:
        while True:
            key = get_key(settings)
            
            if key == 'w':
                node.arm_angle += node.step
            elif key == 's':
                node.arm_angle -= node.step
            elif key == 'a':
                node.bot_angle += node.step
            elif key == 'd':
                node.bot_angle -= node.step
            elif key == ' ' or key == 'x':
                node.bot_angle = 0.0
                node.arm_angle = 0.0
            elif key == '\x03': # CTRL-C
                break
                
            # Giới hạn góc gập cho arm_joint (từ -3.14 đến 3.14)
            if node.arm_angle > 3.14: node.arm_angle = 3.14
            if node.arm_angle < -3.14: node.arm_angle = -3.14
            
            # Gửi lệnh đi
            node.send_angles()
            
            # In ra màn hình để dễ theo dõi
            print(f"\rGóc hiện tại -> Đế: {node.bot_angle:.2f} rad | Tay: {node.arm_angle:.2f} rad", end='')

    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()