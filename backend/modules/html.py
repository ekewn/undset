from functools import partial
from typing import Iterable, Literal
from backend.modules.common import Fn

#
#
# TYPES
#
#


type Html = str
type H1 = Html
type H2 = Html
type Tr = Html
type Tc = Html
type P = Html
type HtmlTag = (Literal["h1"] | Literal["h2"] | Literal["p"] |
                Literal["tr"] | Literal["tc"])
type HtmlComponent = H1 | H2 | P | Tr | Tc


#
#
# FUNCTIONS
#
#


def html(hs: Iterable[HtmlComponent]) -> Html:
    return (
        "Content-Type: text/html"
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<body>"
        f"{"".join(hs)}"
        "</body>"
        "</html>"
    )

h1: Fn[str, H1] = lambda s : f"<h1>{s}</h1>"
h2: Fn[str, H2] = lambda s : f"<h2>{s}</h2>"
tr: Fn[str, Tr] = lambda s : f"<tr>{s}</tr>"
tc: Fn[str, Tc] = lambda s : f"<tc>{s}</tc>"
p : Fn[str, P]  = lambda s: f"<p>{s}</p>"
