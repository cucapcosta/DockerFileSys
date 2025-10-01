import fastapi
from fastapi import FastAPI
from pydantic import BaseModel
import compSystem

app = FastAPI()

class CommandRequest(BaseModel):
    command: str

pcFiles = compSystem.startSystem()
currentFolder = pcFiles
commandList = ["createFolder", "enterFolder", "returnPreviousFolder", "createFile", "writeFile", "readFile", "deleteFile", "deleteFolder", "listContents"]

@app.post("/execute")
def run_pc(request: CommandRequest):
    global pcFiles
    global currentFolder
    command = request.command
    commandParts = command.split(" ")
    match commandParts[0]:
        case "mkdir":
            if len(commandParts) < 2:
                return {"result": "Usage: mkdir <folder_name>"}
            compSystem.createFolder(commandParts[1], currentFolder)
            return {"result": f"Folder '{commandParts[1]}' created."}
        case "cd":
            if len(commandParts) < 2:
                return {"result": "Usage: cd <folder_name>"}
            if( commandParts[1] == ".." ):
                currentFolder = compSystem.returnPreviousFolder(currentFolder, pcFiles)
                return {"result": "Returned to previous folder."}
            newFolder = compSystem.enterFolder(commandParts[1], currentFolder)
            if newFolder:
                currentFolder = newFolder
                return {"result": f"Entered folder '{commandParts[1]}'."}
            else:
                return {"result": f"Folder '{commandParts[1]}' not found."}
        case "touch":
            if len(commandParts) < 2:
                return {"result": "Usage: touch <file_name>"}
            compSystem.createFile(commandParts[1], currentFolder)
            return {"result": f"File '{commandParts[1]}' created."}
        case "write":
            if len(commandParts) < 3:
                return {"result": "Usage: write <file_name> <content>"}
            file = next((f for f in currentFolder.Files if f.name == commandParts[1]), None)
            if file:
                content = " ".join(commandParts[2:])
                compSystem.writeFile(file, content)
                return {"result": f"Written to file '{commandParts[1]}'."}
            else:
                return {"result": f"File '{commandParts[1]}' not found."}
        case "read":
            if len(commandParts) < 2:
                return {"result": "Usage: read <file_name>"}
            file = next((f for f in currentFolder.Files if f.name == commandParts[1]), None)
            if file:
                content = compSystem.readFile(file)
                return {"result": content}
            else:
                return {"result": f"File '{commandParts[1]}' not found."}
        case "rm":
            if len(commandParts) < 2:
                return {"result": "Usage: rm <file_name>"}
            file = next((f for f in currentFolder.Files if f.name == commandParts[1]), None)
            if file:
                compSystem.deleteFile(file, currentFolder)
                return {"result": f"File '{commandParts[1]}' deleted."}
            else:
                return {"result": f"File '{commandParts[1]}' not found."}
        case "rmdir":
            if len(commandParts) < 2:
                return {"result": "Usage: rmdir <folder_name>"}
            folder = next((d for d in currentFolder.Folders if d.name == commandParts[1]), None)
            if folder:
                compSystem.deleteFolder(folder, currentFolder)
                return {"result": f"Folder '{commandParts[1]}' deleted."}
            else:
                return {"result": f"Folder '{commandParts[1]}' not found."}
        case "ls":
            contents = [f.name for f in currentFolder.Folders] + [f.name for f in currentFolder.Files]
            return {"result": "Contents: " + ", ".join(contents)}
        case "current":
            return {"result": f"Current folder: {currentFolder.name}"}
        case _:
            return {"result": f"Unknown command: {commandParts[0]}"}

@app.get("/")
def read_root():
    return {"message": "File System API is running"}