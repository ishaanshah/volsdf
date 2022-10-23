import numpy as np
import argparse
import joblib

def parse_scan(output_camera_file, input_camera_file):
    cam_data = joblib.load(input_camera_file)

    cameras_new = {}
    i = 0
    for _, params in cam_data['0'].items():
        curp = np.eye(4).astype(np.float32)
        curp[:3, :] =  params['extrinsics_opencv']
        cameras_new[f'world_mat_{i}'] = curp.copy()
        i += 1

    np.savez(
        output_camera_file,
        **cameras_new)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parsing STIC camera format')
    parser.add_argument('--input_camera_file', type=str, required=True,
                        help='Path to input camera path')
    parser.add_argument('--output_camera_file', type=str, default="cameras.npz",
                        help='Path to the output file')

    args = parser.parse_args()
    parse_scan(args.output_camera_file, args.input_camera_file)
