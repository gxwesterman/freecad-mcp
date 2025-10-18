"""
TESTING SCRIPT BEFORE DIVING INTO USING THE MCP
"""

import xmlrpc.client

class FreeCADClientServerProxy:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.server = xmlrpc.client.ServerProxy(f"http://{host}:{port}")

    def new_document(self, name: str):
        result = self.server.new_document(name)
        print(f"new_document('{name}'): {result}")
        return result
    
    def get_document(self, name: str):
        result = self.server.get_document(name)
        print(f"get_document('{name}'): {result}")
        return result

    def list_documents(self):
        result = self.server.list_documents()
        print(f"list_documents(): {result}")
        return result
    
    def new_object(self, document_name: str, object_name: str, object_type: str, properties: dict = None):
        if properties is None:
            properties = {}
        result = self.server.new_object(document_name, object_name, object_type, properties)
        print(f"create('{document_name}', '{object_name}', '{object_type}', {properties}): {result}")
        return result
    
    def update_object(self, document_name: str, object_name: str, properties: dict = None):
        result = self.server.update_object(document_name, object_name, properties)
        print(f"update('{document_name}', '{object_name}', {properties}): {result}")
        return result

    def delete_object(self, document_name: str, object_name: str):
        result = self.server.delete_object(document_name, object_name)
        print(f"delete('{document_name}', '{object_name}'): {result}")
        return result
    
    def execute_code(self, code: str):
        result = self.server.execute_code(code)
        print(f"Result: {result}")
        return result

def main():
    try:
        client = FreeCADClientServerProxy()
        # client.new_object("Unnamed", "MyBox", "Part::Box", {
        #     "Length": 20,
        #     "Width": 15,
        #     "Height": 10
        # })

        client.execute_code("""
doc = FreeCAD.newDocument('ExecuteCodeTest')
print(f"Document created: {doc.Name}")
""")

        # client.new_object("Unnamed", "MyFilet", "Part::Fillet", {
        #   "Base": "MyBox",
        #   "Radius": 1,
        #   "Edges": [(1, 1.0, 1.0), (2, 1.0, 1.0), (3, 1.0, 1.0), (4, 1.0, 1.0), (5, 1.0, 1.0), (6, 1.0, 1.0), (7, 1.0, 1.0), (8, 1.0, 1.0), (9, 1.0, 1.0), (10, 1.0, 1.0), (11, 1.0, 1.0), (12, 1.0, 1.0)]
        # })

        # client.update_object("Unnamed", "MyBox", {
        #     "Length": 100,
        #     "Width": 50,
        #     "Height": 12,
        #     "Placement": {
        #         "Base": {"x": 10, "y": 20, "z": 5},
        #         "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 45}
        #     }
        # })
        
        # client.delete_object("Unnamed", "MyBox")

        # client.new_object("Unnamed", "PositionedBox", "Part::Box", {
        #     "Length": 20,
        #     "Width": 15,
        #     "Height": 10,
        #     "Placement": {
        #         "Base": {"x": 10, "y": 20, "z": 5},
        #         "Rotation": {"Axis": {"x": 0, "y": 0, "z": 1}, "Angle": 45}
        #     }
        # })
        
    except ConnectionRefusedError:
        print("Error: Could not connect to FreeCAD RPC Server")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()