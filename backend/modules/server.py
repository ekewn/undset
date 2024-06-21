from http.server import BaseHTTPRequestHandler
from operator import attrgetter
from socketserver import TCPServer
from typing import BinaryIO, Callable, Dict

from common import IO, IOFn, tap
from htmlgen import *

#
#
# DATA
#
#


type Path = str
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


# Header-Related
def _send_response(rc: ResponseCode, self: BaseHTTPRequestHandler) -> IO: return methodcaller("send_response", rc)(self)
_send_200    : IOFn[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, partial(_send_response, 200))
_send_400    : IOFn[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, partial(_send_response, 400))

_send_headers: IOFn[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, methodcaller("send_header", "Content-Type", "text/html; charset = utf-8"))
_end_headers : IOFn[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, methodcaller("end_headers"))

# Write-Related
_wfile       : Fn[BaseHTTPRequestHandler, BinaryIO]     = attrgetter("wfile")
_write       : Fn[BinaryIO, Callable[[bytes], IO]]      = methodcaller("write")
_path        : Fn[BaseHTTPRequestHandler, Path]         = attrgetter("path")
_bytes_utf8  : Fn[str, bytes]                           = partial(bytes, encoding = "utf-8")
_call_rf      : Callable[[Route, RouteFunctions], Html] = lambda x, y: methodcaller("get", x, "404")(y)

#TODO: 
init_response  = compose(_send_200, _send_headers, _end_headers)


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

