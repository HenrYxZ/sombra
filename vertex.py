class Vertex:
    """
    Represent a single vertex which is a single point in world space that has a
    specific material, shader type, normal and (u, v) coordinate for the
    texture.

    Args:
        position(numpy.array): Position in world coordinates
        material(Material): The material to be rendered for this vertex
        shader_type(string): The type of shader to use for this vertex
        normal(numpy.array): The vector normal at this vertex
        u(float): Value for u texture coordinate at this vertex
        v(float): Value for u texture coordinate at this vertex
    """
    def __init__(self, position, material, shader_type, normal, u, v):
        self.position = position
        self.material = material
        self.shader_type = shader_type
        self.normal = normal
        self.u = u
        self.v = v