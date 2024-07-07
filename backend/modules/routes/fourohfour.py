
from htmlgen import *


def main(*args):
    return html([
            h1("where are u try go? dis is err"),
            p(*args)
    ])
