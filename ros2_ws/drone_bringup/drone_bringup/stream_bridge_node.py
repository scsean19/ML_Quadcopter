import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class StreamBridgeNode(Node):
    def __init__(self):
        super().__init__("stream_bridge_node")
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(Image, "/camera/image_raw", 10)
        self.cap = cv2.VideoCapture("tcp://127.0.0.1:8888")

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera TCP stream")

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("Publishing /camera/image_raw from TCP stream")

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Failed to read frame")
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = StreamBridgeNode()
    try:
        rclpy.spin(node)
    finally:
        node.cap.release()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
