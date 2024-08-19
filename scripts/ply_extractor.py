#!/usr/bin/env python3

import open3d as o3d
import numpy as np

def extract_xyz_from_ply(input_ply_file, output_ply_file):
    # Read PLY file using open3d
    pcd = o3d.io.read_point_cloud(input_ply_file)

    # Extract points as numpy array
    points = np.asarray(pcd.points)

    # Write to a new PLY file with only x, y, z values
    with open(output_ply_file, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float32 x\n")
        f.write("property float32 y\n")
        f.write("property float32 z\n")
        f.write("end_header\n")
        
        for point in points:
            f.write(f"{point[0]} {point[1]} {point[2]}\n")

# Example usage:
input_ply_file = '/home/albert/Downloads/Marina_Punat_1M.ply'
output_ply_file = '/home/albert/Downloads/Marina_Punat_1M' + '_v2' + '.ply'

extract_xyz_from_ply(input_ply_file, output_ply_file)
