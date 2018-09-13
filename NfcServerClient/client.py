import requests
import json
def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}
    # Example
    payload = {
       "method": "writeToFile",
       "params": {"token": "user3", "filename": "file.txt", "content": "Hello from user3"},
       "jsonrpc": "2.0",
       "id": 0,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    
    assert response["result"] == "Success"
    assert response["jsonrpc"]
    assert response["id"] == 0

    payload = {
       "method": "getFile",
       "params": {"token": "user2", "filename": "file.txt"},
       "jsonrpc": "2.0",
       "id": 1,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(response["result"])

    assert response["jsonrpc"]
    assert response["id"] == 1

if __name__ == "__main__":
 main()