from dataclasses import dataclass

@dataclass
class File:
    name: str
    content: str
@dataclass
class Folder:
    name: str
    previousFolder: 'Folder'
    Folders: list['Folder']
    Files: list[File]


    
def startSystem() -> Folder:
    root = Folder("/", "", [], [])
    return root
def createFolder(name: str, currentFolder: Folder) -> Folder:
    newFolder = Folder(name, currentFolder, [], [])
    currentFolder.Folders.append(newFolder)
    return newFolder
def enterFolder(name: str, currentFolder: Folder) -> Folder | None:
    for folder in currentFolder.Folders:
        if folder.name == name:
            return folder
    return None
def returnPreviousFolder(currentFolder: Folder, root: Folder) -> Folder:
    if currentFolder.name == root.name:
        return root
    targetFolder = currentFolder.previousFolder
    return targetFolder
def createFile(name: str, currentFolder: Folder) -> File:
    newFile = File(name, "")
    currentFolder.Files.append(newFile)
    return newFile
def writeFile(file: File, content: str) -> None:
    file.content = content
def readFile(file: File) -> str:
    return file.content
def deleteFile(file: File, currentFolder: Folder) -> None:
    currentFolder.Files.remove(file)
def deleteFolder(folder: Folder, currentFolder: Folder) -> None:
    currentFolder.Folders.remove(folder)