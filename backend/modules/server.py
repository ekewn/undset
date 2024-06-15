from socketserver import TCPServer
from http.server import BaseHTTPRequestHandler

from backend.modules.common import IO

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
        if self.path == "/captureImage":
            print("")

        self.send_response(200)

def server_run(n: PortNumber) -> IO:
    """
    Starts up the server.
    """
    TCPServer(("", n), MyHandler).serve_forever()

