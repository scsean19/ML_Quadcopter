import cv2
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

        self.pub = self.create_publisher(
            String,
            "/detections",
            10
        )

        self.sub = self.create_subscription(
            Image,
            "/camera/image_raw",
            self.cb,
            10
        )

        self.annotated_pub = self.create_publisher(
            Image,
            "/camera/yolo_annotated",
            10
        )

        self.get_logger().info("YOLO detector started")

    def draw_dashed_line(
        self,
        image,
        start,
        end,
        color,
        thickness=1,
        dash_length=10
    ):
        x1, y1 = start
        x2, y2 = end

        if y1 == y2:
            for x in range(x1, x2, dash_length * 2):
                cv2.line(
                    image,
                    (x, y1),
                    (min(x + dash_length, x2), y1),
                    color,
                    thickness
                )

        elif x1 == x2:
            for y in range(y1, y2, dash_length * 2):
                cv2.line(
                    image,
                    (x1, y),
                    (x1, min(y + dash_length, y2)),
                    color,
                    thickness
                )

    def cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        results = self.model(frame, verbose=False)

        height, width = frame.shape[:2]

        image_center_x = width // 2
        image_center_y = height // 2

        # Draw dashed center crosshair
        self.draw_dashed_line(
            frame,
            (0, image_center_y),
            (width, image_center_y),
            (255, 255, 255),
            1
        )

        self.draw_dashed_line(
            frame,
            (image_center_x, 0),
            (image_center_x, height),
            (255, 255, 255),
            1
        )

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

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Detected person's center
            cv2.circle(
                frame,
                (person_center_x, person_center_y),
                4,
                (0, 0, 255),
                -1
            )

            # Error vector from image center to target center
            cv2.line(
                frame,
                (image_center_x, image_center_y),
                (person_center_x, person_center_y),
                (0, 0, 255),
                2
            )

            detection = (
                f"person:{best_conf:.2f}, "
                f"center_x:{person_center_x}, "
                f"center_y:{person_center_y}, "
                f"error_x:{error_x}, "
                f"error_y:{error_y}"
            )

            self.pub.publish(String(data=detection))

        # Publish annotated image whether or not a person is detected
        annotated_msg = self.bridge.cv2_to_imgmsg(
            frame,
            encoding="bgr8"
        )

        annotated_msg.header = msg.header
        self.annotated_pub.publish(annotated_msg)


def main(args=None):
    rclpy.init(args=args)

    node = YoloDetectorNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
