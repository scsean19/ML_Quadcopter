import socket
import struct
import threading

import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


HOST = "0.0.0.0"
PORT = 5001


class CameraReceiverNode(Node):

    def __init__(self):
        super().__init__("camera_receiver_node")

        self.publisher_ = self.create_publisher(
            Image,
            "/camera/image_raw",
            10
        )

        self.bridge = CvBridge()
        self.latest_frame = None
        self.frame_lock = threading.Lock()

        self.get_logger().info(f"Starting TCP camera receiver on port {PORT}")

        self.receiver_thread = threading.Thread(
            target=self.receive_frames,
            daemon=True
        )
        self.receiver_thread.start()

        self.timer = self.create_timer(0.1, self.publish_frame)

    def receive_exactly(self, conn, num_bytes):
        data = b""

        while len(data) < num_bytes:
            packet = conn.recv(num_bytes - len(data))

            if not packet:
                return None

            data += packet

        return data

    def receive_frames(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)

            self.get_logger().info("Waiting for camera sender connection...")

            conn, addr = server.accept()

            with conn:
                self.get_logger().info(f"Camera sender connected from {addr}")

                while rclpy.ok():
                    header = self.receive_exactly(conn, 4)

                    if header is None:
                        self.get_logger().warn("Camera sender disconnected")
                        break

                    frame_size = struct.unpack(">I", header)[0]
                    frame_data = self.receive_exactly(conn, frame_size)

                    if frame_data is None:
                        self.get_logger().warn("Incomplete frame received")
                        break

                    np_data = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

                    if frame is None:
                        self.get_logger().warn("Failed to decode JPEG frame")
                        continue

                    with self.frame_lock:
                        self.latest_frame = frame

    def publish_frame(self):
        with self.frame_lock:
            if self.latest_frame is None:
                return

            frame = self.latest_frame.copy()

        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_frame"

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = CameraReceiverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
