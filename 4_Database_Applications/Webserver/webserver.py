from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer

class webserverHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>&#161Hola! <a href='/hello'>Back to Hello</a></body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File not found: %s" % self.path)

def main():
    try:
        port = 8081
        server = SocketServer.TCPServer(('', port), webserverHandler)
        print "Webserver running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping server"
        server.socket.close()


if __name__ == '__main__':
        main()
