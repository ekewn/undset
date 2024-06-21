import os
import sqlite3 as sql
from enum import Enum
from functools import partial
from typing import Iterable, List, Literal, NamedTuple

from backend.modules.common import Fn

#
#
# DATA
#
#


type Id                = int
type Name              = str
type Email             = str
type Password          = str
type Content           = str
type Directory         = str                | os.PathLike
type FilePath          = str                | os.PathLike
type FieldType         = Literal["INTEGER"] | Literal["TEXT"]
type FieldIsPrimaryKey = bool
type FieldIsForeignKey = bool
type FieldIsNullable   = bool
type FieldIsUnique     = bool
type ThreadCreatorId   = int

Field = NamedTuple("Field",
                   [("name", Name)
                   , ("type", FieldType)
                   , ("is_primary_key", FieldIsPrimaryKey)
                   , ("is_foreign_key", FieldIsForeignKey)
                   , ("is_nullable", FieldIsNullable)
                   , ("is_unique", FieldIsUnique)])

Table = NamedTuple("Table", 
                   [("name", Name)
                    , ("fields", List[Field])])

# Table Records

User = NamedTuple("User",
                  [("id", Id)
                    , ("name", Name)
                    , ("email", Email)
                    , ("password", Password)])

Thread = NamedTuple("Thread",
                    [("id", Id)
                    , ("name", Name)
                    , ("creator_id", Id)])

Message = NamedTuple("ThreadMessage",
                      [("id", Id)
                      , ("thread_id", Id)
                      , ("user_id", Id)
                      , ("content", Content)])

# Database Tables

class TABLES(Enum):
    USER = Table(
        "User",
        [
            Field("id",       "INTEGER", True,  False, False, False),
            Field("name",     "TEXT",    False, False, False, True),
            Field("email",    "TEXT",    False, False, False, True),
            Field("password", "TEXT",    False, False, False, False),
        ],
    )
    THREAD = Table(
        "Thread",
        [
            Field("id",         "INTEGER", True,  False, False, False),
            Field("name",       "TEXT",    False, False, False, True),
            Field("creator_id", "INTEGER", False, True,  False, False),
        ],
    )
    THREADMESSAGE = Table(
        "ThreadMessage",
        [
            Field("id",        "INTEGER", True,  False, False, False),
            Field("thread_id", "INTEGER", False, True,  False, False),
            Field("user_id",   "INTEGER", False, True,  False, False),
            Field("content",   "TEXT",    False, False, False, False),
        ],
    )


#
#
# FUNCTIONS
#
#


def _select_all(cur: sql.Cursor, t: TABLES) -> Iterable[User | Thread | Message]:
    results = cur.execute(f"SELECT * FROM {t.name};").fetchall()
    match t:
        case TABLES.USER:
            return map(lambda x: User(x.id, x.name, x.email, x.password), results)
        case TABLES.THREAD:
            return map(lambda x: Thread(x.id, x.name, x.creator_id), results)
        case TABLES.USER:
            return map(lambda x: Message(x.id, x.thread_id, x.user_id, x.content), results)
        case _:
            raise NotImplemented("wot tbl is dis m8?")
select_all_users: Fn[sql.Cursor, Iterable[User]] = partial(_select_all, t=TABLES.USER)
select_all_threads: Fn[sql.Cursor, Iterable[sql.Thread]] = partial(_select_all, t=TABLES.THREAD)
select_all_messages: Fn[sql.Cursor, Iterable[Message]] = partial(_select_all, t=TABLES.THREADMESSAGE)


