from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer

from common import IO
from myhtml import *

#
#
# TYPES
#
#


type PortNumber = int

#
#
# FUNCTIONS
#
#


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"got a hit at {self.path}")
        match self.path.split("/"):
            case ['', '']:
                self.send_response(200, html((h1("Testing"), h2("testing2"))))
            case _:
                self.send_response(400, "where are you trying to go?")

def server_run(n: PortNumber) -> IO:
    """
    Starts up the server.
    """
    TCPServer(("", n), MyHandler).serve_forever()


if __name__ == "__main__":
    server_run(8080)





