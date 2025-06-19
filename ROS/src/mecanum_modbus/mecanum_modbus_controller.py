import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pymodbus.client.serial import ModbusSerialClient
import math

class MecanumModbusController(Node):
    def __init__(self):
        super().__init__('mecanum_modbus_controller')

        # Declare parameters for wheel dimensions and serial port
        self.declare_parameter('wheel_radius', 0.05)     # Radius of wheel in meters
        self.declare_parameter('wheel_base', 0.30)       # Distance between front and rear wheels
        self.declare_parameter('wheel_track', 0.30)      # Distance between left and right wheels
        self.declare_parameter('port', '/dev/ttyUSB0')   # RS485 port

        # Retrieve parameter values
        self.radius = self.get_parameter('wheel_radius').get_parameter_value().double_value
        self.lx = self.get_parameter('wheel_base').get_parameter_value().double_value
        self.ly = self.get_parameter('wheel_track').get_parameter_value().double_value
        self.port = self.get_parameter('port').get_parameter_value().string_value

        # Mapping wheel names to their respective motor Modbus IDs
        self.motor_ids = {
            'front_left': 1,
            'front_right': 2,
            'rear_left': 3,
            'rear_right': 4
        }

        # Initialize Modbus client for RS485 communication
        self.client = ModbusSerialClient(
            method='rtu',
            port=self.port,
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )

        # Attempt to connect to RS485 device
        if not self.client.connect():
            self.get_logger().fatal('Failed to connect to RS485 serial port')
            raise SystemExit

        # Subscribe to /cmd_vel topic to receive velocity commands
        self.subscriber = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.get_logger().info('Mecanum Modbus controller node started')

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocities from Twist message
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z

        # Compute individual wheel RPMs using mecanum kinematics
        wheel_rpms = self.compute_wheel_rpms(vx, vy, wz)

        # Send RPM commands to each motor over Modbus
        self.send_motor_commands(wheel_rpms)

    def compute_wheel_rpms(self, vx, vy, wz):
        r = self.radius
        lx = self.lx
        ly = self.ly

        # Compute unscaled RPM values for each wheel using inverse kinematics
        wheel_speeds = {
            'front_left': (1/r) * (vx - vy - (lx + ly) * wz),
            'front_right': (1/r) * (vx + vy + (lx + ly) * wz),
            'rear_left': (1/r) * (vx + vy - (lx + ly) * wz),
            'rear_right': (1/r) * (vx - vy + (lx + ly) * wz)
        }

        # Convert from rad/s to RPM
        for k in wheel_speeds:
            wheel_speeds[k] = int(wheel_speeds[k] * 60 / (2 * math.pi))

        return wheel_speeds

    def rpm_to_hz(self, rpm):
        # Convert motor shaft RPM to frequency in Hz for the RMCS-3001
        pole_pairs = 4  # 8 poles = 4 pole pairs
        return int((rpm * pole_pairs) / 60)

    def send_motor_commands(self, rpm_dict):
        # Register addresses for the RMCS-3001
        REG_FREQ = 6
        REG_MODE_CTRL = 2
        MODE_DIGITAL_CLOSED_LOOP = 0x0101  # CW direction
        MODE_REVERSE = 0x0109              # CCW direction

        # Loop through each wheel and send speed/direction commands
        for wheel, motor_id in self.motor_ids.items():
            rpm = rpm_dict[wheel]
            hz = self.rpm_to_hz(abs(rpm))
            self.client.write_register(REG_FREQ, hz, slave=motor_id)
            mode = MODE_DIGITAL_CLOSED_LOOP if rpm >= 0 else MODE_REVERSE
            self.client.write_register(REG_MODE_CTRL, mode, slave=motor_id)


def main(args=None):
    rclpy.init(args=args)
    node = MecanumModbusController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Mecanum Modbus controller')
    finally:
        node.client.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
