"""
NOTES:

Tentative FreeCAD object structure (docs are lacking tbh):
{
    'document_name': string,
    'object_name': string,
    'object_type': string (e.g., 'Part::Box', 'Part::Sphere', 'Draft::Circle'),
    'object_properties': {
        'Placement': {
            'Base': {'x': number, 'y': number, 'z': number},
            'Angle': number,
            'Rotation': {'Axis': {'x': number, 'y': number, 'z': number}}
        },
        'ViewObject': {'ShapeColor': [r, g, b, a]},
        'Length': number,
        'Height': number,
        'Width': number,
        'Radius': number,
        ...
    }
}

Tentative Object Types:
- Draft::
    - Line, Polyline, Fillet, Circle, Ellipse, Rectangle, Polygon
- Part::
    - Cube, Cylinder, Sphere, Cone, Torus, Tube
- PartDesign:: (maybe)

"""

import threading
import queue
import FreeCAD

from PySide2 import QtCore
from xmlrpc.server import SimpleXMLRPCServer

class RPCServer:
    
    def __init__(self, host: str = '127.0.0.1', port:int = 8765):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        self.running = False
        self.request_queue = queue.Queue()
    
    def start(self):
        if self.running:
            return False
        
        try:
            self.server = SimpleXMLRPCServer((self.host, self.port), allow_none=True)
            self.server.register_instance(FreeCADRPCMethods(self))
            
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            self.running = True
            
            self._poll()
            
            FreeCAD.Console.PrintMessage(f'FreeCAD RPC Server started on {self.host}:{self.port}\n')
            return True
        except Exception as e:
            FreeCAD.Console.PrintError(f'Failed to start RPC server: {e}\n')
            return False
    
    def _poll(self):
        if not self.running:
            return
        
        try:
            while not self.request_queue.empty():
                func, args = self.request_queue.get_nowait()
                func(*args)
        except Exception as e:
            FreeCAD.Console.PrintError(f'Error in poll: {str(e)}\n')
        
        if self.running:
            QtCore.QTimer.singleShot(10, self._poll)
    
    def _queue(self, func, *args):
        self.request_queue.put((func, args))

    def stop(self):
        if not self.running:
            return False
        
        try:
            if self.server:
                self.server.shutdown()
            self.running = False
            FreeCAD.Console.PrintMessage('FreeCAD RPC Server stopped\n')
            return True
        except Exception as e:
            FreeCAD.Console.PrintError(f'Error stopping RPC server: {e}\n')
            return False

class FreeCADRPCMethods:
    """RPC methods for FreeCAD"""
    
    def __init__(self, rpc_server: RPCServer):
        self.rpc_server = rpc_server

    def new_document(self, name: str = 'Unnamed') -> dict:
        self.rpc_server._queue(self._new_document, name)
        return {'status': 'queued'}
    
    def _new_document(self, name: str) -> dict:
        try:
            doc = FreeCAD.newDocument(name)
            doc.recompute()
            FreeCAD.Console.PrintMessage(f"Document '{name}' created.\n")
            return {'status': 'success', 'document': doc.Name}
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error creating document: {e}\n")
            return {'status': 'error', 'message': str(e)}
    
    def get_document(self, name: str) -> dict:
        try:
            doc = FreeCAD.getDocument(name)
            if doc:
                return {'status': 'success', 'document': doc.Name}
            return {'status': 'error', 'message': 'Document not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def list_documents(self) -> dict:
        try:
            docs = [doc.Name for doc in FreeCAD.listDocuments().values()]
            return {'status': 'success', 'documents': docs}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def new_object(self, document_name: str, object_name: str, object_type: str, properties: dict | None = None) -> dict:
        if properties is None:
            properties = {}
        self.rpc_server._queue(self._new_object, document_name, object_name, object_type, properties)
        return {'status': 'queued'}
    
    def _new_object(self, document_name: str, object_name: str, object_type: str, properties: dict) -> dict:
        try:
            doc = FreeCAD.getDocument(document_name)
            object = doc.addObject(object_type, object_name)
            for key, value in properties.items():

                # Placement has to be set to specific object types
                if key == "Placement":
                    self._set_placement(object, value)
                
                # ShapeColor is a child of ViewObject
                elif key == "ViewObject":
                    self._set_view(object, value)

                # Stuff like fillets are new objects that link to existing objects
                elif key == "Base":
                    base_object = doc.getObject(value)
                    if (base_object):
                        setattr(object, key, base_object)
                        base_object.ViewObject.Visibility = False
                    else:
                        FreeCAD.Console.PrintMessage(f"Base object not found.\n")
                        return {'status': 'error', 'message': 'Base object not found.'}

                # Edges are tuples
                elif key == "Edges" and isinstance(value, list):
                    edge_tuples = [tuple(edge) if isinstance(edge, list) else edge for edge in value]
                    setattr(object, key, edge_tuples)

                # Catch-all
                elif hasattr(object, key):
                    setattr(object, key, value)

            doc.recompute()
            FreeCAD.Console.PrintMessage(f"Object '{object_name}' created.\n")
            return {'status': 'success', 'object': object.Name}
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error creating object: {e}\n")
            return {'status': 'error', 'message': str(e)}
        
    def update_object(self, document_name: str, object_name: str, properties: dict | None = None) -> dict:
        self.rpc_server._queue(lambda: self._update_object(document_name, object_name, properties))
        return {'status': 'queued'}

    def _update_object(self, document_name: str, object_name: str, properties: dict | None = None) -> dict:
        try:
            doc = FreeCAD.getDocument(document_name)
            object = doc.getObject(object_name)
            if not object:
                return {'status': 'error', 'message': 'Object not found.'}

            for key, value in properties.items():

                # Placement has to be set to specific object types
                if key == "Placement":
                    self._set_placement(object, value)
                
                # ShapeColor is a child of ViewObject
                elif key == "ViewObject":
                    self._set_view(object, value)
                
                # Stuff like fillets are new objects that link to existing objects
                elif key == "Base":
                    base_object = doc.getObject(value)
                    if (base_object):
                        setattr(object, key, base_object)
                    else:
                        FreeCAD.Console.PrintMessage(f"Base object not found.\n")
                        return {'status': 'error', 'message': 'Base object not found.'}
                    
                # Catch-all
                elif hasattr(object, key):
                    setattr(object, key, value)

            doc.recompute()
            FreeCAD.Console.PrintMessage(f"Object '{object_name}' updated.\n")
            return {'status': 'success', 'object': object.Name}
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error creating object: {e}\n")
            return {'status': 'error', 'message': str(e)}
    
    def delete_object(self, document_name: str, object_name: str) -> dict:
        self.rpc_server._queue(lambda: self._delete_object(document_name, object_name))
        return {'status': 'queued'}
    
    def _delete_object(self, document_name: str, object_name: str) -> dict:
        try:
            doc = FreeCAD.getDocument(document_name)
            object = doc.getObject(object_name)
            if not object:
                return {'status': 'error', 'message': 'Object not found.'}
            doc.removeObject(object_name)
            doc.recompute()
            FreeCAD.Console.PrintMessage(f"Object '{object_name}' deleted.\n")
        except Exception as e:
            FreeCAD.Console.PrintError(f"Failed to delete '{object_name}'.\n")
            return {'status': 'error', 'message': str(e)}

    def _set_placement(self, object, placement: dict):
        try:
            from FreeCAD import Placement, Vector, Rotation

            base = placement.get('Base', {})
            position = Vector(base.get('x', 0), base.get('y', 0), base.get('z', 0))

            rotation = placement.get('Rotation', {})
            if (rotation):
                axis = rotation.get('Axis', {'x': 0, 'y': 0, 'z': 0})
                angle = rotation.get('Angle', 0)
                axis_vector = Vector(axis['x'], axis['y'], axis['z'])
                if (axis_vector.Length > 0):
                    axis = axis_vector.normalize()
                rotation = Rotation(axis, angle)
            else:
                rotation = Rotation(0, 0, 0)
            
            object.Placement = Placement(position, rotation)
            FreeCAD.Console.PrintMessage(f"Placement set for '{object.Name}'\n")
        except Exception as e:
            FreeCAD.Console.PrintError(f"Failed to set placement: {e}\n")
    
    def _set_view(self, object, view: dict):
        try:
            for key, value in view.items():

                # The value of ShapeColor has to be a tuple (L)
                if key == "ShapeColor":
                    setattr(object.ViewObject, key, (float(value[0]), float(value[1]), float(value[2]), float(value[3])))
                else:
                    setattr(object.ViewObject, key, value)
        except Exception as e:
            FreeCAD.Console.PrintError(f"Failed to set view properties: {e}\n")

    def execute_code(self, code: str) -> dict:
        self.rpc_server._queue(self._execute_code, code)
        return {'status': 'queued'}
    
    def _execute_code(self, code: str) -> dict:
        try:
            namespace = {
                'FreeCAD': FreeCAD,
                'App': FreeCAD,
                'doc': None
            }
            
            try:
                namespace['doc'] = FreeCAD.activeDocument()
            except:
                pass
            
            exec(code, namespace)
            
            FreeCAD.Console.PrintMessage(f"Code executed successfully.\n")
            return {'status': 'success', 'message': 'Code executed'}
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error executing code: {e}\n")
            return {'status': 'error', 'message': str(e)}

rpc_server = RPCServer()

class StartRPCServerCommand:
    
    def GetResources(self):
        return {
            'MenuText': 'Start MCP RPC Server',
            'ToolTip': 'tooltip'
        }
    
    def Activated(self):
        rpc_server.start()
    
    def IsActive(self):
        return not rpc_server.running


class StopRPCServerCommand:
    
    def GetResources(self):
        return {
            'MenuText': 'Stop RPC Server',
            'ToolTip': 'whatever'
        }
    
    def Activated(self):
        rpc_server.stop()
    
    def IsActive(self):
        return rpc_server.running
