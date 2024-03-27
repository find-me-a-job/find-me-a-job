from http.server import BaseHTTPRequestHandler, HTTPServer

# Define the HTTP request handler class
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        if(self.path == "/getdata"):
            # Set response status code
            self.send_response(200)
            # Set headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Write response content
            self.wfile.write(b"<html><head><title>Sample HTTP Server</title></head>")
            self.wfile.write(b"<body><h1>Hello, World!</h1></body></html>")
        else:
            # Set response status code
            self.send_response(200)
            # Set headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Write response content
            self.wfile.write(b"<html><head><title>Sample HTTP Server</title></head>")
            self.wfile.write(b"<body><h1>Hello, World!</h1></body></html>")

# Define the main function to start the server
def main():
    try:
        server = HTTPServer(('localhost', 8080), MyHTTPRequestHandler)
        print('HTTP server started on http://localhost:8080')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the server')
        server.socket.close()

# Entry point of the script
if __name__ == '__main__':
    main()
