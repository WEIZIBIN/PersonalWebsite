from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import cgi
import json


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/chat.html'

        prefix = '/webpage'
        self.path = prefix + self.path

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith('.html'):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith('.jpg'):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith('.gif'):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith('.js'):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith('.css'):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):

        if self.path == '/xiaoice':
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            if ctype == 'application/json':
                length = int(self.headers['content-length'])
                post_values = json.loads(self.rfile.read(length))
            else:
                post_values = {}


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    run()

if __name__ == '__main__':
    main()