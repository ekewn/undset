from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Dict

from pyamda import IO
from htmlgen import *

#
#
# DATA
#
#


type Route = str
type RouteFunctions = Dict[Route, Html]


ROUTEFUNCTIONS: RouteFunctions = {"/": html((h1("Testing"), h2("testing2"))),
                                  "404": html(h1("Where were you trying to go?"))}

#
#
# FUNCTIONS
#
#

# Handler
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> IO:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset = utf-8")
        self.end_headers()
        self.wfile.write(bytes(ROUTEFUNCTIONS.get(self.path, "404"), "utf-8"))


#
#
# TEST
#
#


if __name__ == "__main__":
    TCPServer(("", 8080), MyHandler).serve_forever()
