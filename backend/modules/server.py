from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Dict, List, Optional

from routes import fourohfour, root
from pyamda import IO
from htmlgen import *

#
#
# DATA
#
#


type Route = str
type RouteFunctions = Dict[Route, Html]
type Param = str
type Arg = str
type QueryStrings = Optional[Dict[Param, Arg]]

#
#
#
# FUNCTIONS
#
#

def query_params(url:Route) -> QueryStrings:
    """
    Get the query params as a dictionary, if present, on the url.
    """
    query_params_exist = "/?" in url
    if not query_params_exist: return None
    queries = url.split("/?")[1]
    return dict([q.split("=") for q in queries.split("&")]) if query_params_exist else None


def route(route: Route, query_strings: QueryStrings) -> Html:
    """
    Handles the calling of each route and passing of parameters when applicable.
    """
    return (
        root.main() if route == "/"
        else fourohfour.main(query_strings)
        
    )


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> IO:
        """
        Handles all get requests from the client.
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset = utf-8")
        self.end_headers()
        self.html = route(self.path, query_params(self.path))
        self.wfile.write(bytes(self.html, "utf-8"))


#
#
# TEST
#
#


if __name__ == "__main__":
    TCPServer(("", 8080), Handler).serve_forever()
