"""Turn in place to face the closest object within 25 cm.

Run inside the robot software's container:  python3 face_closest.py
Stop with Ctrl+C.
"""
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

MAX_DISTANCE = 0.25  # meters: ignore anything further away
TURN_SPEED = 1.0     # radians per second, at most
ON_TARGET = math.radians(5)  # close enough: stop turning


def robot_angle(scan, i):
    """Angle of scan point i as seen by the robot: 0 = straight ahead, + = left, - = right.

    The robot's LiDAR is mounted upside down, so its angles run the other way around,
    starting from the back. 180 degrees minus the scan angle fixes both.
    """
    a = math.pi - (scan.angle_min + i * scan.angle_increment)
    return math.atan2(math.sin(a), math.cos(a))  # wrap to -180..180 degrees


class FaceClosest(Node):
    def __init__(self):
        super().__init__('face_closest')
        self.cmd = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(LaserScan, 'scan', self.on_scan, qos_profile_sensor_data)

    def on_scan(self, scan):
        # Find the closest valid point within MAX_DISTANCE.
        closest, angle = MAX_DISTANCE, None
        for i, r in enumerate(scan.ranges):
            if scan.range_min < r < closest:
                closest, angle = r, robot_angle(scan, i)
        twist = Twist()
        if angle is not None:
            print(f'closest: {closest:.2f} m at {math.degrees(angle):4.0f} degrees')
            if abs(angle) > ON_TARGET:
                # Turn toward it: left for positive angles, right for negative ones.
                twist.angular.z = max(-TURN_SPEED, min(TURN_SPEED, 2.0 * angle))
        self.cmd.publish(twist)  # an empty Twist means "stop"


def main():
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)  # we handle Ctrl+C ourselves
    node = FaceClosest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.cmd.publish(Twist())  # stop the wheels before exiting
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
