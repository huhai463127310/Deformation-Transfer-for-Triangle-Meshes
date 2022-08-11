import trimesh
import numpy as np
import json
import meshio
from gen_makers_yaml import batch_convert_wrap_point_to_vertex_id

def cacluate_barycentric_weight(mesh, face_id, px, py):
    
    print(mesh.faces[face_id])

    x = [0]
    x.extend([mesh.vertices[v][0] for v in mesh.faces[face_id]])
    y = [0]
    y.extend([mesh.vertices[v][1] for v in mesh.faces[face_id]])

    print(x, y)

    w1 = ((y[2] - y[3]) * (px - x[3]) + (x[3] - x[2]) * (py - y[3])) / ((y[2] - y[3]) * (x[1] - x[3]) + (x[3] - x[2]) * (y[1] - y[3]))
    w2 = ((y[3] - y[1]) * (px - x[3]) + (x[1] - x[3]) * (py - y[3])) / ((y[2] - y[3]) * (x[1] - x[3]) + (x[3] - x[2]) * (y[1] - y[3]))
    w3 = 1 - w1 - w2
    
    print(((y[2] - y[3]) * (px - x[3]) + (x[3] - x[2]) * (py - y[3])), ((y[2] - y[3]) * (x[1] - x[3]) + (x[3] - x[2]) * (y[1] - y[3])))
    return np.array([w1, w2, w3])

def cacluate_cartesian_coordinates(mesh, face_id, px, py):
    weights = cacluate_barycentric_weight(mesh, face_id, px, py)
    print(weights)
    points = np.array([mesh.vertices[vertex_id] for vertex_id in mesh.faces[face_id]])
    print(points)
    new_point = np.sum(points * np.array(weights), axis = 0)
    print(new_point)

def convert_wrap_point_to_vertex_id(mesh, face_id, px, py):
    print(mesh.faces[face_id])
    return mesh.faces[face_id][np.argmin([px, py])]

def test_convert_wrao_point_to_vertex_id(json_file):
    with open(json_file, mode="r") as f:
        wrap_points = json.load(f)
    
    vertex_ids = list()
    for wrap_point in wrap_points:
        vertex_id = convert_wrap_point_to_vertex_id(anna_mp_mesh, *wrap_point)
        vertex_ids.append(vertex_id)
    print(vertex_ids)

def check_mesh():
    anna_mp_mesh = trimesh.load_mesh("models\Anna\mp\Anna_MP.obj")
    anna_mh_mesh = trimesh.load_mesh("models\Anna\mh\AnnaNakedHead-triangle-2.obj")

    face_id = 9873
    print(anna_mh_mesh.faces[face_id])

    # scene = trimesh.Scene(anna_mh_mesh)
    # scene.add_geometry(trimesh.PointCloud([anna_mh_mesh.vertices[v] for v in anna_mh_mesh.faces[face_id]], colors=[255,0,0,255]))
    # scene.show()
    
    mh_mesh = meshio.read("models\Anna\mh\AnnaNakedHead-triangle-2.obj")
    # mh_mesh = meshio.read("D:\DigitalHuman\Anna\obj\AnnaNakedHead-triangle-2.obj")
    print(mh_mesh)

    

if __name__ == "__main__":
    anna_mp_mesh = trimesh.load_mesh("models\Anna\mp\Anna_MP.obj")
    anna_mh_mesh = trimesh.load_mesh("models\Anna\mh\AnnaNakedHead-triangle-2.obj")
    
    wrap_point = [0, 0.0043732523918151855, 0.08745219558477402]
    # wrap_point = [551, 0.010681331157684326, 0.005213988479226828]
    # wrap_point_3d = {
    #     "x": -1.7549700736999512,
    #     "y": -0.028902340680360794,
    #     "z": 2.9370386600494385
    # }

    # vertex_id = convert_wrao_point_to_vertex_id(anna_mp_mesh, *wrap_point)
    # print(vertex_id)

    # triangle_json_file = "models\Anna\mp\mp-points_on_triangle.json"
    # xyz_json_file = "models\Anna\mp\mp-points_3d-2.json"
    # ids_save_path = "models\Anna\mp\mp-points_id.json"
    # mesh = anna_mp_mesh

    # cacluate_cartesian_coordinates(mesh, *wrap_point)

    params = [
        (anna_mp_mesh, "models\Anna\mp\mp-points_on_triangle.json", "models\Anna\mp\mp-points_3d-2.json", "models\Anna\mp\mp-points_id.json"),
        (anna_mh_mesh, "models\Anna\mh\mh-points_on_triangle-3.json", "models\Anna\mh\mh-points_3d-3.json", "models\Anna\mh\mh-points_id.json")]
    for mesh, triangle_json_file, xyz_json_file, ids_save_path in params:
        batch_convert_wrap_point_to_vertex_id(mesh, triangle_json_file, xyz_json_file, ids_save_path)

    
    