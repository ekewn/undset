from functools import partial
from operator import methodcaller
from typing import Iterable, Literal, Tuple

from common import Fn, compose

#
#
# TYPES
#
#


type Link          = str
type Html          = str
type H1            = Html
type H2            = Html
type Th            = Html
type Td            = Html
type Tr            = Html
type Table         = Html
type A             = Html
type P             = Html
type Text          = Html
type HtmlComponent = H1 | H2 | P | Tr | Td
type HtmlTag       = (Literal["h1"] | Literal["h2"] | Literal["p"] |
                      Literal["tr"] | Literal["td"] | Literal["a"] |
                      Literal["th"])


#
#
# FUNCTIONS
#
#


join: Fn[Iterable[str], str] = lambda _: methodcaller("join", _)("")


def html(hs: Iterable[HtmlComponent]) -> Html:
    return (
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<body>"
        f"{join(hs)}"
        "</body>"
        "</html>"
    )


def _htmlComponent(t: HtmlTag, s: str | HtmlComponent) -> HtmlComponent:
    return f"<{t}>{s}</{t}>"
h1 :  Fn[str, H1] = partial(_htmlComponent, "h1")
h2 :  Fn[str, H2] = partial(_htmlComponent, "h2")
p  :  Fn[str, P]  = partial(_htmlComponent, "p")
_th:  Fn[str, Th] = partial(_htmlComponent, "th")
_td:  Fn[str, Td] = partial(_htmlComponent, "td")
_tr:  Fn[str, Tr] = partial(_htmlComponent, "tr")


_wrap_rows = lambda x: compose(partial(map,x), join, _tr)
_wrap_th   = _wrap_rows(_th)
_wrap_td   = _wrap_rows(_td)


def th(headers: Iterable[str]) -> Tr: return _wrap_th(headers)


def td(rows: Iterable[str]) -> Tr: return _wrap_td(rows)


def a(content: str, link: Link) -> A: return f"<a href={link}>{content}</a>"


def table(headers: Iterable[Td], rows: Iterable[Tuple]) -> Table:
    return f"<table>{th(headers)}{join(map(td,rows))}</table>"


#
#
# TEST
#
#
if __name__ == "__main__":
    print_html = compose(html, print)
    print_html(table(["h1", "h2", "h3"]
                      , [("td11", "td12", "td13"),
                         ("td21", "td22", "td23")]))
