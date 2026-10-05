"""Follow the closest object in front of the robot, staying 40 cm away.

Run inside the robot software's container:  python3 follow_me.py
Stop with Ctrl+C.
"""
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

KEEP_DISTANCE = 0.40   # meters: how far behind to stay
SEE_DISTANCE = 1.00    # meters: ignore anything further away
SEE_ANGLE = math.radians(30)  # look 30 degrees to each side of straight ahead
MAX_SPEED = 0.15       # meters per second
MAX_TURN = 1.0         # radians per second


def robot_angle(scan, i):
    """Angle of scan point i as seen by the robot: 0 = straight ahead, + = left, - = right.

    The robot's LiDAR is mounted upside down, so its angles run the other way around,
    starting from the back. 180 degrees minus the scan angle fixes both.
    """
    a = math.pi - (scan.angle_min + i * scan.angle_increment)
    return math.atan2(math.sin(a), math.cos(a))  # wrap to -180..180 degrees


class FollowMe(Node):
    def __init__(self):
        super().__init__('follow_me')
        self.cmd = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(LaserScan, 'scan', self.on_scan, qos_profile_sensor_data)

    def on_scan(self, scan):
        # Find the closest point in the cone in front of the robot.
        closest, angle = SEE_DISTANCE, None
        for i, r in enumerate(scan.ranges):
            a = robot_angle(scan, i)
            if abs(a) < SEE_ANGLE and scan.range_min < r < closest:
                closest, angle = r, a
        twist = Twist()
        if angle is not None:
            print(f'following: {closest:.2f} m at {math.degrees(angle):4.0f} degrees')
            # Drive to close the gap (back up if too close) and steer toward the target.
            twist.linear.x = max(-MAX_SPEED, min(MAX_SPEED, 0.8 * (closest - KEEP_DISTANCE)))
            twist.angular.z = max(-MAX_TURN, min(MAX_TURN, 2.0 * angle))
        self.cmd.publish(twist)  # nothing in sight: stop


def main():
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)  # we handle Ctrl+C ourselves
    node = FollowMe()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.cmd.publish(Twist())  # stop the wheels before exiting
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
