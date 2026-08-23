import rclpy
from rclpy.node import Node

import sys
import select
import termios
import tty

from std_msgs.msg import String



#INFO 
#Keys : WASD ; UHJK
#Step Motor Order for coiling: (m1,m2,m3,m4) = (Front motor - W, Right Motor - D , Back Motor - S , Left Motor - A) its Clockwise starting from front motor
#Step Motor Order for Uncoiling : (m1,m2,m3,m4) = (Front motor - U, Right Motor - K , Back Motor - H , Left Motor - J) its Clockwise starting from front motor


class FourMotorTeleop(Node):

    def __init__(self):
        super().__init__('four_motor_teleop')

        # One topic carrying commands for all four motors.
        self.motor_publisher = self.create_publisher(
            String,
            '/motor_commands',
            10
        )

        # Save terminal configuration so that we can restore it later.
        self.settings = termios.tcgetattr(sys.stdin)

        self.get_logger().info('Four Motor Teleop Started')
        self.get_logger().info('W = FRONT')
        self.get_logger().info('S = BACK')
        self.get_logger().info('A = Left')
        self.get_logger().info('D = Right')
        self.get_logger().info('X = Stop')
        self.get_logger().info('Q = Quit')

    def get_key(self):

        # Put terminal into raw mode.
        tty.setraw(sys.stdin.fileno())

        key = sys.stdin.read(1)

        # Restore terminal configuration.
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.settings
        )

        return key

    def send_motor_command(self, m1, m2, m3, m4):

        msg = String()

        msg.data = (
            f"M1:{m1} "
            f"M2:{m2} "
            f"M3:{m3} "
            f"M4:{m4}"
        )

        self.motor_publisher.publish(msg)

        self.get_logger().info(msg.data)

    def process_key(self, key):

        key = key.lower()

        if key == 'w':

            # COIL
            self.send_motor_command(
                "COIL",
                "STOP",
                "STOP",
                "STOP"
            )

        elif key == 's':

            # UNCOIL
            self.send_motor_command(
                "STOP",
                "STOP",
                "COIL",
                "STOP"
            )

        elif key == 'a':

            # Turn left
            self.send_motor_command(
                "STOP",
                "STOP",
                "STOP",
                "COIL"
            )

        elif key == 'd':

            # Turn right
            self.send_motor_command(
                "STOP",
                "COIL",
                "STOP",
                "STOP"
            )

        elif key == 'u':

            # COIL
            self.send_motor_command(
                "UNCOIL",
                "STOP",
                "STOP",
                "STOP"
            )

        elif key == 'j':

            # UNCOIL
            self.send_motor_command(
                "STOP",
                "STOP",
                "UNCOIL",
                "STOP"
            )

        elif key == 'h':

            # Turn left
            self.send_motor_command(
                "STOP",
                "STOP",
                "STOP",
                "UNCOIL"
            )

        elif key == 'k':

            # Turn right
            self.send_motor_command(
                "STOP",
                "UNCOIL",
                "STOP",
                "STOP"
            )


        elif key == 'x':

            # Stop
            self.send_motor_command(
                "STOP",
                "STOP",
                "STOP",
                "STOP"
            )

        elif key == 'q':

            self.send_motor_command(
                "STOP",
                "STOP",
                "STOP",
                "STOP"
            )

            return False

        self.get_logger().info(key)
        return True

    def run(self):

        running = True

        try:

            while running and rclpy.ok():

                key = self.get_key()

                running = self.process_key(key)

                # ros2 will process callbacks so giving it 0.01secs
                rclpy.spin_once(self, timeout_sec=0.01)

        finally:

            # Stopping all motors if the program exits.
            self.send_motor_command(
                "STOP",
                "STOP",
                "STOP",
                "STOP"
            )

            # Back to original terminal
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                self.settings
            )


def main(args=None):

    rclpy.init(args=args)

    node = FourMotorTeleop()

    try:
        node.run()

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()