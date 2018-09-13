import os
import errno
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import methods

@dispatcher.add_method
def getFile(token, filename):
    return methods.getFile(token, filename)

@dispatcher.add_method
def write(token, filename, content):
    return methods.writeToFile(token, filename, content)

@Request.application
def application(request):
     # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response( response.json, mimetype='application/json')

if __name__ == '__main__':
    run_simple('localhost', 4000, application)