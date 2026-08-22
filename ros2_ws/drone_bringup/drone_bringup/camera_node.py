import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from picamera2 import Picamera2
import time

class CameraPublisher(Node):

	def __init__(self):
		super().__init__('camera_publisher')

		self.get_logger().info("Starting Camera Publisher Node")

		#Create Publisher
		self.publisher_ = self.create_publisher(
			Image,
			'/camera/image_raw',
			10
		)
		
		#Create CvBridge
		self.bridge = CvBridge()

		#Initialize Camera
		self.picam2 = Picamera2()
		config = self.picam2.create_preview_configuration(
			main={"size":(640,480)}
		)
		
		self.picam2.configure(config)

		self.picam2.start()

		time.sleep(2)

		#Timer for Publishing Frames
		self.timer = self.create_timer(
			.1, #10Hz
			self.timer_callback
		)


	def timer_callback(self):

		frame = self.picam2.capture_array()
		msg = self.bridge.cv2_to_imgmsg(
			frame,
			encoding="bgr8"
		)

		self.publisher_.publish(msg)

def main(args=None):

	rclpy.init(args=args)
	node = CameraPublisher()

	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.picam2.stop()
		node.destroy_node()
		rclpy.shutdown()

if __name__ == '__main__':
	main()
