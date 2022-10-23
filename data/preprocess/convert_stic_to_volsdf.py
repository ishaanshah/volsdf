import os
import numpy as np
import argparse
import joblib
from tqdm import tqdm
from normalize_cameras import normalize_cameras


parser = argparse.ArgumentParser(description='Parsing STIC camera format')
parser.add_argument('--data', type=str, required=True,
                    help='Path to input data')

args = parser.parse_args()

print("Converting camera parameters")
cam_data = joblib.load(os.path.join(args.data, "cam_data.pkl"))

cameras_new = {}
cam_names = []
for cam_name, cam_params in cam_data['0'].items():
    if not os.path.exists(os.path.join(args.data, "image", cam_name)):
        continue

    intr = np.eye(4).astype(np.float32)
    intr[0,0] = cam_params['K'][0]
    intr[1,1] = cam_params['K'][1]
    intr[0,2] = cam_params['K'][2]
    intr[1,2] = cam_params['K'][3]

    extr = np.eye(4).astype(np.float32)
    extr[:3, :] = cam_params['extrinsics_opencv']

    curp = intr @ extr

    cameras_new[f'world_mat_{len(cam_names)}'] = curp.copy()
    cam_names.append(cam_name)

np.savez(
    os.path.join(args.data, "cameras_unnormalized.npz"),
    **cameras_new
)

print("Normalizing camera parameters")
normalize_cameras(
    os.path.join(args.data, "cameras_unnormalized.npz"),
    os.path.join(args.data, "cameras.npz"), -1
)

print("Symlinking images")
i = 0
for cam_name in tqdm(cam_names):
    target_name = os.path.join(args.data, "image", f"{i:05d}.png")
    if os.path.exists(target_name):
        os.remove(target_name)
    os.symlink(
            os.path.join(cam_name, "00000.png"),
            target_name
        )
    i += 1
