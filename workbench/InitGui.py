"""
APPARENTLY THIS IS A FILE FREECAD NEEDS - INIT GUI STUFF
"""

import FreeCADGui

class FreeCADRCPServerWorkbench(FreeCADGui.Workbench):
    MenuText = "MCP RCP Server"
    ToolTip = "A custom RCP server addon for MCP communication"

    def Initialize(self):
        from RPCServerWorkbench import StartRPCServerCommand, StopRPCServerCommand

        FreeCADGui.addCommand("StartRPCServer", StartRPCServerCommand())
        FreeCADGui.addCommand("StopRPCServer", StopRPCServerCommand())

        self.appendToolbar("MCP RCP Server", ["StartRPCServer", "StopRPCServer"])
        self.appendMenu("MCP RCP Server", ["StartRPCServer", "StopRPCServer"])

    def Activated(self):
        pass

    def Deactivated(self):
        pass

FreeCADGui.addWorkbench(FreeCADRCPServerWorkbench())