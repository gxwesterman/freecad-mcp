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
    
client = FreeCADClientServerProxy()

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
    
    Args:
        document_name: Name of the FreeCAD document
        object_name: Name for the new object
        object_type: FreeCAD object type (e.g., 'Part::Box', 'Part::Sphere', 'Draft::Circle')
        properties: Dictionary of object properties (Length, Width, Height, Radius, etc.)
    
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
    """Update the properties of an existing FreeCAD object"""
    result = client.update_object(document_name, object_name, properties)
    return json.dumps(result)


@mcp.tool()
def delete_object(document_name: str, object_name: str) -> str:
    """Delete an existing FreeCAD object"""
    result = client.delete_object(document_name, object_name)
    return json.dumps(result)


def main():
    mcp.run()

if __name__ == "__main__":
    main()