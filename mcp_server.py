"""
BASIC MCP SERVER
"""

from mcp.server.fastmcp import FastMCP
import xmlrpc.client
import json

mcp = FastMCP("FreeCAD")

class FreeCADClientServerProxy:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.server = xmlrpc.client.ServerProxy(f"http://{host}:{port}")

    def new_document(self, name: str):
        return self.server.new_document(name)
    
    def get_document(self, name: str):
        return self.server.get_document(name)

    def list_documents(self):
        return self.server.list_documents()
    
    def new_object(self, document_name: str, object_name: str, object_type: str, properties: dict = None):
        if properties is None:
            properties = {}
        return self.server.new_object(document_name, object_name, object_type, properties)
    
    def update_object(self, document_name: str, object_name: str, properties: dict = None):
        return self.server.update_object(document_name, object_name, properties)

    def delete_object(self, document_name: str, object_name: str):
        return self.server.delete_object(document_name, object_name)
    
    def update_edges(self, document_name: str, base_object_name: str, edge_type: str, edges):
        return self.server.update_edges(document_name, base_object_name, edge_type, edges)
    
    def create_sketch(self, document_name: str, sketch_name: str, plane: str = "XY"):
        return self.server.create_sketch(document_name, sketch_name, plane)

    def add_sketch_circle(self, document_name: str, sketch_name: str, center_x: float, center_y: float, radius: float):
        return self.server.add_sketch_circle(document_name, sketch_name, center_x, center_y, radius)

    def add_sketch_rectangle(self, document_name: str, sketch_name: str, x1: float, y1: float, x2: float, y2: float):
        return self.server.add_sketch_rectangle(document_name, sketch_name, x1, y1, x2, y2)

    def extrude(self, document_name: str, pad_name: str, sketch_name: str, length: float, symmetric: bool = False):
        return self.server.extrude(document_name, pad_name, sketch_name, length, symmetric)
    
    def execute_code(self, code: str):
        return self.server.execute_code(code)
    
client = FreeCADClientServerProxy()

@mcp.prompt()
def freecad_instructions() -> str:
    """
    Instructions on creating assets in FreeCAD:
    1. The following are basic objects:
      - Draft::
        - Line, Polyline, Fillet, Circle, Ellipse, Rectangle, Polygon
      - Part::
        - Cube, Cylinder, Sphere, Cone, Torus, Tube
    2. To create basic objects, use new_object
    3. To change existing basic objects, use update_object
    4. To apply fillets or chamfers, use update_edges
    5. TO extrude, use create_sketch, then add_sketch_*, then extrude
    6. To delete basic objects or edges (e.g. fillets or chamfers), use delete_object
    7. For everything else, create a script and use execute_code
    """

@mcp.tool()
def create_document(name: str = "Unnamed") -> str:
    """Create a new FreeCAD document"""
    result = client.new_document(name)
    return json.dumps(result)

@mcp.tool()
def get_document(name: str) -> str:
    """Get a document by name"""
    result = client.get_document(name)
    return json.dumps(result)

@mcp.tool()
def list_documents() -> str:
    """List all open FreeCAD documents"""
    result = client.list_documents()
    return json.dumps(result)

@mcp.tool()
def create_object(document_name: str, object_name: str, object_type: str, properties: dict | None = None ) -> str:
    """
    Create a new object in a FreeCAD document
    
    Arguments:
      document_name: name of the FreeCAD document
      object_name: name for the new object
      object_type: FreeCAD object type (e.g., 'Part::Box', 'Part::Sphere', 'Draft::Circle')
      properties: dictionary of object properties (Length, Width, Height, Radius, etc.)
    
    Returns:
      JSON string with status and object name

    Examples:
      To create a light pink cone with a height of 50, radius of 30, you can use the following data:
      
      document_name: 'MyDocument',
      object_name: 'MyCone',
      object_type: 'Part::Cone',
      properties: {
        "Height": 50,
        "Radius1": 30,
        "Radius2": 0,
        "Angle": 360,
        "Placement": {
          "Base": {
            "x": 0,
            "y": 0,
            "z": 0
          },
          "Rotation": {
            "Axis": {
              "x": 0,
              "y": 0,
              "z": 1
            },
            "Angle": 180
          }
        },
        "ViewObject": {
          "ShapeColor": [1.0, 0.75, 0.80, 1.0]
        }
      }

    """
    result = client.new_object(document_name, object_name, object_type, properties)
    return json.dumps(result)

@mcp.tool()
def update_object(document_name: str, object_name: str, properties: dict | None = None) -> str:
    """
    Updates the properties of an existing FreeCAD object

    Arguments:
      document_name: the name of the document on which to update the object
      object_name: the name of the object to update
      properties: dictionary of object properties (Length, Width, Height, Radius, etc.)

    Examples:
      To create a light pink cone with a height of 50, radius of 30, you can use the following data:
      
      document_name: 'MyDocument',
      object_name: 'MyCone',
      object_type: 'Part::Cone',
      properties: {
        "Height": 50,
        "Radius1": 30,
        "Radius2": 0,
        "Angle": 360,
        "Placement": {
          "Base": {
            "x": 0,
            "y": 0,
            "z": 0
          },
          "Rotation": {
            "Axis": {
              "x": 0,
              "y": 0,
              "z": 1
            },
            "Angle": 180
          }
        },
        "ViewObject": {
          "ShapeColor": [1.0, 0.75, 0.80, 1.0]
        }
      }

    Returns:
      JSON string with status and object name
    """
    result = client.update_object(document_name, object_name, properties)
    return json.dumps(result)

@mcp.tool()
def delete_object(document_name: str, object_name: str) -> str:
    """
    Delete an existing FreeCAD object

    Arguments:
      document_name: the name of the document from which to delete the object
      object_name: the name of the object to delete

    Returns:
      JSON string with status and object name
    """
    result = client.delete_object(document_name, object_name)
    return json.dumps(result)

# Claude has no idea what is required for Edges
@mcp.tool()
def update_edges(document_name, base_object_name, edge_type, edges) -> str:
    """
    Updates the edges on a FreeCAD object

    Arguments:
      document_name: the name of the document upon which to create the new edge object
      base_object_name: the base object that the edge object references
      edge_type: the FreeCAD object type of edge to add (either Part::Fillet or Part::Chamfer)
      edges: an array of edges e.g. [[1, 1.0, 1.0], [2, 1.0, 1.0], ...]

    Returns:
      JSON string with status and object name
    
    Examples:
      To add a fillet to every edge on a cube, you can use the following data:

      document_name: 'MyDocument',
      base_object_name: 'MyCube',
      edge_type: 'Part::Fillet'
      edges: [[1, 1.0, 1.0], [2, 1.0, 1.0], [3, 1.0, 1.0], [4, 1.0, 1.0], [5, 1.0, 1.0], [6, 1.0, 1.0], [7, 1.0, 1.0], [8, 1.0, 1.0], [9, 1.0, 1.0], [10, 1.0, 1.0], [11, 1.0, 1.0], [12, 1.0, 1.0]]
    """
    result = client.update_edges(document_name, base_object_name, edge_type, edges)
    return json.dumps(result)

@mcp.tool()
def create_sketch(document_name: str, sketch_name: str, plane: str = "XY") -> str:
    '''Create a new sketch on a plane (XY, XZ, or YZ)'''
    result = client.create_sketch(document_name, sketch_name, plane)
    return json.dumps(result)

@mcp.tool()
def add_sketch_circle(document_name: str, sketch_name: str, center_x: float, center_y: float, radius: float) -> str:
    '''
    Add a circle to a sketch
    
    Example:
      document_name: 'MyDocument'
      sketch_name: 'Sketch'
      center_x: 0
      center_y: 0
      radius: 5
    '''
    result = client.add_sketch_circle(document_name, sketch_name, center_x, center_y, radius)
    return json.dumps(result)

@mcp.tool()
def add_sketch_rectangle(document_name: str, sketch_name: str, x1: float, y1: float, x2: float, y2: float) -> str:
    '''
    Add a rectangle to a sketch (defined by two opposite corners)
    
    Example:
      document_name: 'MyDocument'
      sketch_name: 'Sketch'
      x1: 0
      y1: 0
      x2: 10
      y2: 5
    '''
    result = client.add_sketch_rectangle(document_name, sketch_name, x1, y1, x2, y2)
    return json.dumps(result)

@mcp.tool()
def extrude(document_name: str, pad_name: str, sketch_name: str, length: float, symmetric: bool = False) -> str:
    '''Extrude (Pad) a sketch into a 3D solid'''
    result = client.extrude(document_name, pad_name, sketch_name, length, symmetric)
    return json.dumps(result)

@mcp.tool()
def execute_code(code: str) -> str:
    """
    Executes code on the FreeCAD server

    Arguments:
      code: arbritrary Python code to execute

    Returns:
      JSON string with status and object name
    """
    result = client.execute_code(code)
    return json.dumps(result)


def main():
    mcp.run()


if __name__ == "__main__":
    main()