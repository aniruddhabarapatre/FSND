from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Getting all the restaurants
            if self.path.endswith("/restaurants"):
                results = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                for restaurant in results:
                    output += restaurant.name
                    output += "<br>"
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "<br><br><br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Create new restaurant
            if self.path.endswith("/restaurants/new"):
                results = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'restaurantname' type = 'text'> "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File not found: %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurantname')

                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

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
