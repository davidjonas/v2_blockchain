from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os
from threading import Thread

PORT_NUMBER = 8888
HOST_NAME = "localhost"
BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'UI'

class myHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".woff2"):
                mimetype='application/font-woff2'
                sendReply = True
            if self.path.endswith(".woff"):
                mimetype='application/font-woff'
                sendReply = True
            if self.path.endswith(".ttf"):
                mimetype='application/x-font-truetype'
                sendReply = True
            if self.path.endswith(".ico"):
                mimetype='image/x-icon'
                sendReply = True
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True



            if sendReply == True:
                #Open the static file requested and send it
                f = open(BASE_PATH + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
        except IOError:
            self.send_error(404,'File Not Found: %s' % BASE_PATH + self.path)

    def log_message(self, format, *args):
        return

class UIServer(Thread):
    def __init__(self):
        super(UIServer, self).__init__()
        self.server = HTTPServer((HOST_NAME, PORT_NUMBER), myHandler)
        self.killed = False
        self.daemon = True

    def run(self):
        while not self.killed:
            self.server.handle_request()


    def kill(self):
        self.server.socket.close()
        self.killed = True
