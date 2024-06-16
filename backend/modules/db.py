from enum import Enum
import os
from typing import List, Literal, NamedTuple
import sqlite3 as sql

from backend.scripts.db_create import TABLES

#
#
# DATA
#
#


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
def select_all(cur: sql.Cursor, t: TABLES):
    cur
