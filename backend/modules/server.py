from http.server import BaseHTTPRequestHandler
from operator import attrgetter
from socketserver import TCPServer
from typing import BinaryIO, Callable, Dict

from pyamda import IO, get, tap
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
_send_200    : FnU[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, partial(_send_response, 200))
_send_400    : FnU[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, partial(_send_response, 400))

_send_headers: FnU[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, methodcaller("send_header", "Content-Type", "text/html; charset = utf-8"))
_end_headers : FnU[BaseHTTPRequestHandler, BaseHTTPRequestHandler] = partial(tap, methodcaller("end_headers"))

# Write-Related
_wfile       : FnU[BaseHTTPRequestHandler, BinaryIO] = attrgetter("wfile")
_write       : FnU[BinaryIO, Callable[[bytes], IO]]  = partial(methodcaller("write"), _wfile)
_path        : FnU[BaseHTTPRequestHandler, Path]     = attrgetter("path")
_bytes_utf8  : FnU[str, bytes]                       = partial(bytes, encoding = "utf-8")
_call_rf     : FnU[Route, Html]                      = partial(get, ROUTEFUNCTIONS, "404")

# Pipelines
init_response = compose(_send_200, _send_headers, _end_headers)
write_html    = compose(_path, _call_rf, _bytes_utf8, _write)


# Handler
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> IO:
        init_response(self)
        write_html(self)


def server_run(n: PortNumber) -> IO:
    TCPServer(("", n), MyHandler).serve_forever()


#
#
# MAIN
#
#


if __name__ == "__main__":
    server_run(8080)



