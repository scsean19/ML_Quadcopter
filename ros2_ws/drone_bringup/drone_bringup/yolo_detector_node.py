import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO


class YoloDetectorNode(Node):
    def __init__(self):
        super().__init__("yolo_detector_node")
        self.bridge = CvBridge()
        self.model = YOLO("yolov8n.pt")
        self.pub = self.create_publisher(String, "/detections", 10)
        self.sub = self.create_subscription(Image, "/camera/image_raw", self.cb, 10)
        self.get_logger().info("YOLO detector started")

    def cb(self, msg):
    frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
    results = self.model(frame, verbose=False)

    height, width = frame.shape[:2]
    image_center_x = width // 2
    image_center_y = height // 2

    best_person = None
    best_conf = 0.0

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = self.model.names[cls_id]

        if class_name == "person" and conf > 0.5:
            if conf > best_conf:
                best_conf = conf
                best_person = box

    if best_person is not None:
        x1, y1, x2, y2 = best_person.xyxy[0].cpu().numpy()

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        person_center_x = (x1 + x2) // 2
        person_center_y = (y1 + y2) // 2

        error_x = person_center_x - image_center_x
        error_y = person_center_y - image_center_y

        detection = (
            f"person:{best_conf:.2f}, "
            f"center_x:{person_center_x}, "
            f"center_y:{person_center_y}, "
            f"error_x:{error_x}, "
            f"error_y:{error_y}"
        )

        self.pub.publish(String(data=detection))


def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
