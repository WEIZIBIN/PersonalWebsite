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
            self.send_error(404, 'Not Found: %s' % self.path)

    def do_POST(self):

        sendReply = False

        if self.path == '/xiaoice':
            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            if ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers['content-length'])
                post_values = self.rfile.read(length)
                sendReply = True

        try:

            if sendReply:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'retCode':'0'}
                response_json = json.dumps(response)
                self.wfile.write(bytes(response_json, 'UTF8'))

        except IOError:
            self.send_error(404, 'Not Found: %s' % self.path)



def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    run()

if __name__ == '__main__':
    main()