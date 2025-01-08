def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/ping':
        data = b'pong\n'
        status = '200 OK'
    else:
        data = b'Not Found\n'
        status = '404 Not Found'

    start_response(status, [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ])
    return iter([data])

    



