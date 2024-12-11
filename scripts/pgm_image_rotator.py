#!/usr/bin/env python3

import os
import sys
import rclpy
from PIL import Image
from rclpy.node import Node

class PGMImage(Node):
    def __init__(self):
        super().__init__("pgm_image_rotator")
        image_file_path = "/home/albert/marinero_ws/src/marinero_simulations/config/marina_punat_map/marina_punat_v2.pgm"

        try:
            image = Image.open(image_file_path)
            rotated_image = image.rotate(90, expand=True)

            new_file_path = os.path.splitext(image_file_path)[0] + "_correlated.pgm"

            rotated_image.save(new_file_path)

            self.get_logger().info(f"Successfully rotated the image and saved it as {new_file_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to rotate the image: {str(e)}")
        sys.exit(1)

def main(args=None):
    rclpy.init(args=args)
    node = PGMImage()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()