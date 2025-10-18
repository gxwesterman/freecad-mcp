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
        result = self.server.new_document(name)
        return result
    
    def get_document(self, name: str):
        result = self.server.get_document(name)
        return result

    def list_documents(self):
        result = self.server.list_documents()
        return result
    
    def new_object(self, document_name: str, object_name: str, object_type: str, properties: dict | None = None):
        result = self.server.new_object(document_name, object_name, object_type, properties)
        return result
    
    def update_object(self, document_name: str, object_name: str, properties: dict | None = None):
        result = self.server.update_object(document_name, object_name, properties)
        return result
    
    def delete_object(self, document_name: str, object_name: str):
        result = self.server.delete_object(document_name, object_name)
        return result
    
    def execute_code(self, code: str):
        result = self.server.execute_code(code)
        return result
    
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
    4. For everything else, create a script and use execute_code
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


@mcp.tool
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