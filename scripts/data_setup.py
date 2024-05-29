import os
import sqlite3
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Literal, NamedTuple

#
#
# DATA
#
#

# Globals
SCRIPT_DIR_PATH = os.path.dirname(__file__)
ROOT_DIR = Path(SCRIPT_DIR_PATH).parent.absolute()
DB_NAME = os.path.join(ROOT_DIR,"backend","db.db")
HS_NAME = os.path.join(ROOT_DIR,"backend","src","DataDefs.hs")
ELM_NAME = os.path.join(ROOT_DIR,"frontend","src","DataDefs.elm")

# Type Aliases
type Fn[a, b] = Callable[[a], b]
type Id = int
type Name = str
type Email = str
type Password = str
type Content = str
type Sql = str
type Succeeded = bool
type Directory = str | os.PathLike
type FilePath = str | os.PathLike
type TableFields = list[Field]
type FieldType = Literal["INTEGER"] | Literal["TEXT"]
type FieldIsPrimaryKey = bool
type FieldIsForeignKey = bool
type FieldIsNullable = bool
type FieldIsUnique = bool
type ThreadCreatorId = int
type HsType = Literal["String"] | Literal["Integer"] | Literal["Boolean"]
type HsTypeDef = str
type HsDataDef = str
type ElmType = Literal["String"] | Literal["Int"] | Literal["Bool"]
type ElmTypeDef = str
type ElmDataDef = str

# Types
Table = NamedTuple("Table" , [("name", Name) , ("fields", TableFields)])
Field = NamedTuple("Field",
                   [("name", Name)
                   , ("type", FieldType)
                   , ("is_primary_key", FieldIsPrimaryKey)
                   , ("is_foreign_key", FieldIsForeignKey)
                   , ("is_nullable", FieldIsNullable)
                   , ("is_unique", FieldIsUnique)])
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

# Database Table Structures
class TABLES(Enum):
    """
    Metadata for each table in the database.
    """
    USER = Table("User",
                 [Field("id", "INTEGER", True, False, False, False)
                  , Field("name", "TEXT", False, False, False, True)
                  , Field("email", "TEXT", False, False, False, True)
                  , Field("password", "TEXT", False, False, False, False)])
    THREAD = Table("Thread",
                   [Field("id", "INTEGER", True, False, False, False)
                   , Field("name", "TEXT", False, False, False, True)
                   , Field("creator_id", "INTEGER", False, True, False, False)])
    MESSAGE = Table("ThreadMessage",
                      [Field("id", "INTEGER", True, False, False, False)
                      , Field("thread_id", "INTEGER", False, True, False, False)
                      , Field("user_id", "INTEGER", False, True, False, False)
                      , Field("content", "TEXT", False, False, False, False)])

#
#
# DATA
#
#

# Test Data
test_users: list[User] = [
    User(1, "admin", "ellis.coon@gmail.com", "admin")
]

test_threads: list[Thread] = [
    Thread(1, "test", 1)
]

test_messages: list[Message] = [
    Message(1, 1, 1, "first message")
    , Message(2, 1, 1, "second message")
]


#
#
# FUNCTIONS
#
#

# Generalized
consume: Fn[Iterator, deque] = \
lambda _: deque(_, maxlen=0)

join_to_comma: Fn[Iterator[str], str] = \
lambda _: ", ".join(list(_))

# Type Specific
table_name: Fn[TABLES, Name] = \
lambda _: _.value.name

# SQL Generators
def table_create_sql(t: TABLES) -> Sql:
    any_foreign_keys: bool = any(list(map(lambda f: f.is_foreign_key, t.value.fields))) 
    foreign_keys: list[Name] = list(
        map(lambda f: f.name, filter(lambda f: f.is_foreign_key, t.value.fields)))

    return ( 
        f" CREATE TABLE IF NOT EXISTS {t.name} ( "
        f" {join_to_comma(map(field_create_sql, t.value.fields))} "
        f" {", " + join_to_comma(map(foreign_key_create_sql, foreign_keys)) if any_foreign_keys else ''}"
        ");")


def foreign_key_create_sql(f_name: Name) -> Sql:
    t_name: Name = f_name.split("_")[0]

    return f" FOREIGN KEY ({f_name}) REFERENCES {t_name.title()} (id) "


def field_create_sql(f: Field) -> Sql:
    is_primary_key: str = "PRIMARY KEY" if f.is_primary_key else ""
    is_unique: str = "UNIQUE" if f.is_unique else ""
    is_nullable : str = "" if f.is_nullable else "NOT NULL"

    return f"{f.name} {f.type} {is_primary_key} {is_nullable} {is_unique} "


# Haskell Generators
hs_str: Fn[Any, HsType | Any] = \
lambda _: "String" if isinstance(_, str) else _

hs_bool: Fn[Any, HsType | Any] = \
lambda _: "Boolean" if isinstance(_, bool) else _

hs_int: Fn[Any, HsType | Any] = \
lambda _: "Integer" if isinstance(_, int) else _

hs_type_determine: Fn[Any, HsType | Any] = \
lambda _: hs_int(hs_bool(hs_str(_)))

hs_type_return: Fn[Any, HsType] = \
lambda _: hs_type_determine(_) if hs_type_determine(_) != _ else "String"

hs_field_type_generate: Fn[Field, HsTypeDef] = \
lambda _: f"  {_.name} :: {hs_type_return(_.type)}"


def hs_data_create(t: TABLES) -> HsDataDef:
    t_name = table_name(t)
     return (
        f"{{- Definition constructed from {t_name} type in {__file__} -}}\n"
        f"data {t_name} = {t_name}\n"
        "  { \n"
        f"    {join_to_comma(map(hs_field_type_generate, t.value.fields))}\n"
        "  }\n\n"
    )


def hs_file_create(target_filename: FilePath) -> Succeeded:
    try:
        with open(target_filename, "w") as f:
            f.write(f"module DataDef( )where \n")
            list(map(f.write, map(hs_data_create, TABLES)))
        return True

    except Exception as e:
        print(e)
        return False


# Elm Generators
elm_str: Fn[Any, ElmType | Any] = \
lambda _: "String" if isinstance(_, str) else _

elm_bool: Fn[Any, ElmType | Any] = \
lambda _: "Bool" if isinstance(_, bool) else _

elm_int: Fn[Any, ElmType | Any] = \
lambda _: "Int" if isinstance(_, int) else _

elm_type_determine: Fn[Any, ElmType | Any] = \
lambda _: elm_int(elm_bool(elm_str(_)))

elm_type_return: Fn[Any, ElmType] = \
lambda _: elm_type_determine(_) if elm_type_determine(_) != _ else "String"

elm_field_type_generate: Fn[Field, ElmTypeDef] = \
lambda _: f" {_.name} : {elm_type_return(_.type)}"


def elm_data_create(t: TABLES) -> ElmDataDef:
    t_name = table_name(t)
    return (
        f"{{- Definition constructed from {t_name} type in {__file__} -}}\n"
        f"{t_name} : {{ {join_to_comma(map(elm_field_type_generate, t.value.fields))} }}"
        "\n\n"
    )


def elm_file_create(target_filename: FilePath) -> Succeeded:
    try:
        with open(target_filename, "w") as f:
            f.write("module DataDef where \n")
            list(map(f.write, map(elm_data_create, TABLES)))
        return True
    except Exception as e:
        print(e)
        return False
#
#
# MAIN
#
#
if __name__ == "__main__":
    cur = sqlite3.connect(DB_NAME).cursor()
    scripts_table_create = list(map(table_create_sql, TABLES))
    list(map(cur.executescript, scripts_table_create))
    cur.close()

    hs_file_create(HS_NAME)

    elm_file_create(ELM_NAME)



