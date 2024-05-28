import sqlite3
from typing import Literal

#
#
# DATA
#
#
type Result = Literal["Success"] | Literal["Failure"]

TABLES: list[str] = ["Users", "Threads", "Messages"]

def init() -> sqlite3.Connection:
    return sqlite3.connect("test.db")

def table_create(cx: sqlite3.Connection, name: str) -> sqlite3.Connection:
    cx.
    return cx
