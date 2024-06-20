from http.server import BaseHTTPRequestHandler
from operator import attrgetter
from socketserver import TCPServer
from typing import Callable, Dict

from common import IO, IOFn, tap
from htmlgen import *

#
#
# DATA
#
#


type ResponseCode = int
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


# Generic
call_rf: Callable[[Route, RouteFunctions], Html] = lambda x, y: methodcaller("get", x, "404")(y)

# Header-Related
def _send_response(rc: ResponseCode, self: BaseHTTPRequestHandler) -> IO:
    return methodcaller("send_response", rc)(self)
_send_200: IOFn[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, partial(_send_response, 200))
_send_400: IOFn[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, partial(_send_response, 400))
_send_headers  = partial(tap, methodcaller("send_header", "Content-Type", "text/html; charset = utf-8"))
_end_headers   = partial(tap, methodcaller("end_headers"))

# Write-Related
_wfile = attrgetter("wfile")
_write = methodcaller("write")
_path = attrgetter("path")
_bytes_utf8 = partial(bytes, encoding="utf-8")

#TODO: 
init_response  = compose(_send_200, _send_headers, _end_headers, _wfile )


# Handler
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self, rf: RouteFunctions = ROUTEFUNCTIONS) -> IO:
        init_response(self)
        self.wfile.write(bytes(call_rf(_path(self), rf), "utf-8"))


def server_run(n: PortNumber) -> IO:
    TCPServer(("", n), MyHandler).serve_forever()


#
#
# MAIN
#
#


if __name__ == "__main__":
    server_run(8080)

