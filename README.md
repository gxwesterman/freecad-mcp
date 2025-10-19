## SETUP
a. FreeCAD Setup
  1. Clone the repository: `https://github.com/gxwesterman/freecad-mcp.git`
  2. Copy the FreeCAD workbench to the correct folder:
      - Windows: `<UserFolder>\AppData\Roaming\FreeCAD\Mod\`
      - Linux: `~/.FreeCAD/Mod/` or `~/.local/share/FreeCAD/Mod/`
  3. Restart FreeCAD
  4. Select the MCP RCP Server workbench and start the server
  
      <img width="752" height="253" alt="image" src="https://github.com/user-attachments/assets/72c1db90-3f18-4cb5-babb-ad052836d301" />

b. Claude Setup
  1. Add the MCP server to your Claude desktop config
  
      ```json
      {
        "mcpServers": {
          "freecad": {
            "command": "uv",
            "args": [
              "--directory",
              "C:\\Users\\gwesterman.NAGIOS\\repos\\freecad-mcp-test",
              "run",
              "mcp_server.py"
            ]
          }
        }
      }
      ```
  
     - Windows: `code $env:AppData\Claude\claude_desktop_config.json`
     - MacOS\Linux: `code ~/Library/Application\ Support/Claude/claude_desktop_config.json`
  2. Restart Claude Desktop
  3. Ask Claude to make stuff in FreeCAD - it'll do its best

## RUN INSTRUCTIONS
The MCP can:
- List available documents
- Get the current document
- Create, edit, and delete basic objects
- Add edges to objects
- Roughly extrude
- Execute arbritrary code of its own making

## Quickstart Example
Paste the following queries into a Claude Desktop chat:

```
Create a cube in the current FreeCAD document
```
```
Create a pink cone
```
```
Replace the cone with a long cylinder at a 90 degree angle
```
```
Fillet the edges of the cube
```
