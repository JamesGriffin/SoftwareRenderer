class IndexedMesh(object):
    """Represents a mesh loaded from a provided obj"""
    def __init__(self, obj_filename):
        self.vertices = []
        self.normals = []
        self.faces = []

        with open(obj_filename) as fp:
            for line in fp:

                data_type = line.split(" ")[0]

                if data_type == "v":
                    x, y, z = line.split(" ")[1:]
                    self.vertices.append([float(x), float(y), float(z), 1])

                if data_type == "vn":
                    x, y, z = line.split(" ")[1:]
                    self.normals.append([float(x), float(y), float(z)])

                if data_type == "f":

                    if line.split(" ")[1:].__len__() > 3:
                        raise IOError("Unsupported mesh - only triangulated meshes are supported.")

                    v1, v2, v3 = line.split(" ")[1:]
                    self.faces.append([
                        int(v1.split("/")[0]),
                        int(v2.split("/")[0]),
                        int(v3.split("/")[0])
                     ])

