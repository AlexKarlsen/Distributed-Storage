import os
import glob
import shutil
import requests
import json

url = "http://localhost:4000/jsonrpc"
headers = {'content-type': 'application/json'}

def recursive_copy_files(source_path, destination_path, override=False, subfolderCounter=-1):
#
#Recursively copies files from source  to destination directory.
#:param source_path: source directory
#:param destination_path: destination directory
#:param override if True all files will be overwritten otherwise skip if file exist
#:return: count of copied files
#

    files_count = 0

    if not os.path.exists(destination_path):
        #os.mkdir(destination_path)
        subfolder = source_path.split('/')[subfolderCounter]
        response = requests.post(url, data=json.dumps({"method": "createDir", "params": { "dirname": subfolder.join}}))


    items = glob.glob(source_path + '/*')

    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            subfolderCounter += -1
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override, subfolderCounter=subfolderCounter)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            if not os.path.exists(file) or override:
                #Copy file
                shutil.copyfile(item, file)
                files_count += 1

    return files_count

    
    # Example
    payload = {
       "method": "writeToFile",
       "params": {"filename": "file.txt", "content": "Hello from user3"},
       "jsonrpc": "2.0",
       "id": 0,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    
    assert response["result"] == "Success"
    assert response["jsonrpc"]
    assert response["id"] == 0

if __name__ == "__main__":
    recursive_copy_files("./test", "./replica_test_1", override = False)
    recursive_copy_files("./test", "./replica_test_2", override = False)
