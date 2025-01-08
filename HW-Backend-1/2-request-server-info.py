import json 

def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/info':
        data = {
            'method': environ['REQUEST_METHOD'],
            'url': environ['PATH_INFO'],
            'protocol': environ['SERVER_PROTOCOL'],
        }
        data = json.dumps(data).encode('utf-8')
        status = '200 OK'
    else:
        data = b'Not Found\n'
        status = '404 Not Found'
        
    start_response(status, [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ])
    return [data] 

    



