import os

def getFile(filepath):
    #Exception handling
    if not os.path.exists(filepath):
        return "File not found"

    with open(filepath, "r") as f:
        return f.read()

def writeToFile(filename, content):
    #Exception handling
    if not os.path.exists(filename):
        with open(filename, "w+") as f:
            f.write(content)
    else:
        with open(filepath, "a") as f:
            f.write(content)
    
    return "Success"

def createDir(dirname):
    if not os.path.exists(dirname)
        os.mkdir(dirname)
