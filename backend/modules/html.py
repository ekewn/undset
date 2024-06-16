from typing import Iterable, Literal
from functools import partial

from common import Fn

#
#
# TYPES
#
#


type Html          = str
type H1            = Html
type H2            = Html
type Tr            = Html
type Tc            = Html
type P             = Html
type Text          = Html
type HtmlComponent = H1 | H2 | P | Tr | Tc
type HtmlTag       = (Literal["h1"] | Literal["h2"] | Literal["p"] |
                      Literal["tr"] | Literal["tc"])


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


def _htmlComponent(t: HtmlTag, s: str | HtmlComponent) -> HtmlComponent:
    return f"<{t}>{s}</{t}>"
h1:  Fn[str, H1] = partial(_htmlComponent, "h1")
h2:  Fn[str, H2] = partial(_htmlComponent, "h2")
tr:  Fn[str, Tr] = partial(_htmlComponent, "tr")
tc:  Fn[str, H1] = partial(_htmlComponent, "tc")
p :  Fn[str, H2] = partial(_htmlComponent, "p")
