import os
import json
import sys
import BaseHTTPServer


Welcome = "\n***\nWelcome to Simple Transfer Over GaVer Server\n***\n\n"
j = { 'commands': [ 'list', 'stor', 'retr' ], 'srvmsg': Welcome, 'srvauth':'password' }




class RequestHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(j))
        return

    def do_POST(self):
	var = self.headers
	self.send_response(200)
	self.end_headers()
	self.wfile.write({'filename':'tito.jpg'})
        return	

    def _get_status (self):
        return os.getloadavg()

def main (args):
    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', 8000), RequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
