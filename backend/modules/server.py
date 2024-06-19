from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Dict

from common import IO
from htmlgen import *

#
#
# DATA
#
#


type PortNumber = int
type Route = str
type RouteFunctions = Dict[Route, Html]

ROUTEFUNCTIONS: RouteFunctions = {"/": html((h1("Testing"), h2("testing2"))),
                                  "404": html(h1("Where were you trying to go?"))}

#
#
# FUNCTIONS
#
#
dict.get

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self, rf: RouteFunctions = ROUTEFUNCTIONS) -> IO:
        self.send_response(200, "Hit root")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(rf.get(self.path, "Where are u going m8?"), "utf-8"))


def server_run(n: PortNumber) -> IO:
    TCPServer(("", n), MyHandler).serve_forever()


#
#
# MAIN
#
#


if __name__ == "__main__":
    server_run(8080)
