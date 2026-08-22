import socket
import struct
import time

import cv2
from picamera2 import Picamera2


HOST = "127.0.0.1"
PORT = 5001
WIDTH = 320
HEIGHT = 240
JPEG_QUALITY = 60
FPS_DELAY = 0.1  # ~10 Hz


def main():
    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={"size": (320, 240), "format": "BGR888"}
    )

    picam2.configure(config)
    picam2.start()
    time.sleep(2)

    print(f"Connecting to ROS receiver at {HOST}:{PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connected. Sending frames...")

        frame_count = 0

        try:
            while True:
                frame = picam2.capture_array()

                success, encoded = cv2.imencode(
                    ".jpg",
                    frame,
                    [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
                )

                if not success:
                    print("JPEG encode failed")
                    continue

                data = encoded.tobytes()
                header = struct.pack(">I", len(data))

                sock.sendall(header + data)

                frame_count += 1

                if frame_count % 30 == 0:
                    print(f"Sent {frame_count} frames")

                time.sleep(FPS_DELAY)

        except KeyboardInterrupt:
            print("\nStopping sender...")

        finally:
            picam2.stop()


if __name__ == "__main__":
    main()

