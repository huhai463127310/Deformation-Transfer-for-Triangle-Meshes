import json
import yaml
import os
from collections import OrderedDict
import trimesh
import math
import numpy as np


def load_points(point_json_file):
    points = list()
    with open(point_json_file, mode="r") as f:
        json_data = json.load(f)
        for point_info in json_data:
            point_no, _, _ = point_info
            points.append(point_no)
    return points 

def load_markers(mesh_file_path, triangle_json_file, xyz_json_file):
    mesh = trimesh.load_mesh(mesh_file_path)
    return batch_convert_wrap_point_to_vertex_id(mesh, triangle_json_file, xyz_json_file)

def load_poses(pose_dir, pose_path_prefix):
    files = os.listdir(pose_dir)
    obj_files = [file for file in files if file.endswith(".obj")]
    return [os.path.join(pose_path_prefix, file) for file in obj_files]

def batch_convert_wrap_point_to_vertex_id(mesh, triangle_json_file, xyz_json_file, save_path=None):
    with open(triangle_json_file, mode="r") as f:
        wrap_points = json.load(f)

    with open(xyz_json_file, mode="r") as f:
        wrap_points_3d = json.load(f)

    ids = list()
    for wrap_point, wrap_point_3d in zip(wrap_points, wrap_points_3d):
        face_id, px, py = wrap_point
        points = np.array([mesh.vertices[vertex_id] for vertex_id in mesh.faces[face_id]])
        distances = list()
        for point in points:
            
            distance = math.sqrt(pow(point[0] - wrap_point_3d["x"], 2) + pow(point[1] - wrap_point_3d["y"], 2) + pow(point[2] - wrap_point_3d["z"], 2))
            distances.append(distance)
        
        min_distance_idx = np.argmin(np.array(distances))
        ids.append((int)(mesh.faces[face_id][min_distance_idx]))

    if save_path:
        with open(save_path, mode="w+") as f:
            json.dump(ids, f)        
        print("points ids save at file {}".format(save_path))
    return ids    
   

if __name__ == "__main__":
    yaml_data = {
        "source":{"reference":"mp\Anna_MP.obj", "poses":[]},
        "target":{"reference":"mh\AnnaNakedHead.obj", "poses":[]},
    }

    # mp_points = load_points("models\Anna\mp\mp-points_on_triangle.json")
    # mh_points = load_points("models\Anna\mh\mh-points_on_triangle.json")

    mp_points = load_markers("models\Anna\mp\Anna_MP.obj", "models\Anna\mp\mp-points_on_triangle.json", "models\Anna\mp\mp-points_3d-2.json")
    mh_points = load_markers("models\Anna\mh\AnnaNakedHead-triangle-2.obj", "models\Anna\mh\mh-points_on_triangle-3.json", "models\Anna\mh\mh-points_3d-3.json")

    mp_poses = load_poses("models\Anna\mp\mp-poses", "mp\mp-poses")
    mh_poses = [pose_path.replace("mp\mp-poses", "mh\mh-poses") for pose_path in mp_poses]

    markers = ["{}:{}".format(*pair) for pair in zip(mp_points, mh_points)]

    yaml_data["source"]["poses"] = mp_poses
    yaml_data["target"]["poses"] = mh_poses
    yaml_data["markers"] = markers

    yaml_file_path = os.path.join(os.path.dirname(__file__), "markers-Anna-mp-mh.yml")
    with open(yaml_file_path, mode="w+") as f:
        yaml.dump(yaml_data, f)
    print("yaml file save at {}".format(yaml_file_path))
