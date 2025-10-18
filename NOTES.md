### PROCESS
- Started by researching MCPs. I have never heard of them until a couple days prior. Dylan had cryptically texted me something like "Thinking of making an MCP server" with no additional context.
- Went to the MCP website and read through the intro docs and the tutorial. Decided the route of least resistance would probably be to:
  1. Develop on Windows (yuck) because that's the only OS I have with a GUI so I can run everything locally.
  2. Use Claude Desktop as the MCP client. The tutorial uses it and it's free and presumably well-tested.
- Googled "free CAD software" and the first result was FreeCAD so I ran with that. I briefly looked into the other options to see if anything would be better suited but nothing stood out. FreeCAD looked like it had some examples and a robust enough API.
- Installed Claude
- Ran through the MCP tutorial to ensure everything worked. At this point, I wasn't 100% sure that Anthropic still supported MCPs on their free version. Some forum posts said they didn't. Evidently they do. Probably a skill issue.
- Researched how to interact with the FreeCAD API programatically. Turns out they have a couple Python libraries. Quickly realized that interacting with the API directly would have to be headless and if I wanted to see changes live I would have to set up an internal server that communicates with the MCP. Bummer. Thankfully FreeCAD has support for addons.
- Created an extremely basic workbench to start/stop an RCP server that interacts directly with FreeCAD. Created some tests.
  - Started with just listing documents. Easy.
  - Tried to create a document - FreeCAD explodes. 