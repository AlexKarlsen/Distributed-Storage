import os

def getFile(token, filename):
    filepath = token + "/" + filename
    
    #Exception handling
    if not os.path.exists(filepath):
        return "File not found"

    with open(filepath, "r") as f:
        return f.read()

def writeToFile(token, filename, content):
    filepath = token + "/" + filename

    #Exception handling
    if not os.path.exists(filepath):
        with open(filepath, "w+") as f:
            f.write(content)
    else:
        with open(filepath, "a") as f:
            f.write(content)
    
    return "Success"