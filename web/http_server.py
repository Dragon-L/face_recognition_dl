from http.server import HTTPServer, SimpleHTTPRequestHandler


def start_http_server(port):
    httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print('Server is on port:', port)
    httpd.serve_forever()


start_http_server(8080)