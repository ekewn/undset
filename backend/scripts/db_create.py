import os
import sqlite3 as sql
from pathlib import Path
from typing import Any, Iterator, List, Literal

from modules.common import IO, consume
from modules.db import (TABLES, Field, FilePath, Message, Name, Table, Thread,
                        User)

#
#
# DATA
#
#

# Globals
THIS_DIR  = os.path.dirname(__file__)
PROJ_ROOT = Path(THIS_DIR).parent.parent.absolute() # Assumes this is in a scripts dir /proj-root/backend/scripts/thisfile.py
DB_NAME   = os.path.join(PROJ_ROOT,"backend","db.db")
ELM_NAME  = os.path.join(PROJ_ROOT,"frontend","src","Tables.elm")

# Test Data
test_users   : List[User] = [User(1, "admin", "ellis.coon@gmail.com", "admin")]

test_threads : List[Thread] = [Thread(1, "test", 1)]

test_messages: List[Message] = [
    Message(1, 1, 1, "first message"),
    Message(2, 1, 1, "second message"),
]



#
#
# FUNCTIONS
#
#

# Helper
def join_to_comma(i: Iterator[str]) -> str:
    return ", ".join(list(i))


# SQL Generators
type Sql = str
type SqlTable = str
type SqlField = str
type SqlForeignKey = str

def sqlField(f: Field) -> SqlField:
    is_primary_key: str = "PRIMARY KEY" if f.is_primary_key else ""
    is_unique: str = "UNIQUE" if f.is_unique else ""
    is_nullable : str = "NOT NULL" if not f.is_nullable else ""

    return " ".join([f.name, f.type, is_primary_key, is_nullable, is_unique])


def sqlForeignKey(f_name: Name) -> SqlForeignKey:
    t_name: Name = f_name.split("_")[0]

    return f" FOREIGN KEY ({f_name}) REFERENCES {t_name.title()} (id) "


def sqlTable(t: Table) -> SqlTable:
    """
    Generates the SQL create statement for a table.
    """
    any_foreign_keys: bool = any(map(lambda f: f.is_foreign_key, t.fields))
    foreign_keys: List[Name] = list(map(lambda x: x.name, filter(lambda f: f.is_foreign_key, t.fields)))

    return ( 
        f" CREATE TABLE {t.name} ( "
        f" {join_to_comma(map(sqlField, t.fields))} "
        f" {", " + join_to_comma(map(sqlForeignKey, foreign_keys)) if any_foreign_keys else ''}"
        ");")


# Generic Generator 
type TypeDef = HsTypeDef | ElmTypeDef
type Types = HsTypes | ElmTypes


def types(str_repr: Types, bool_repr: Types, int_repr: Types, x: Any) -> Types:
    """
    Allows for the creation of string representations for Python data types in other languages.
    """
    def str_(x: Any) -> Types | Any:
        return str_repr if isinstance(x, str) else x
    def bool_(x: Any) -> Types | Any:
        return bool_repr if isinstance(x, bool) else x
    def int_(x: Any) -> Types | Any:
        return int_repr if isinstance(x, int) else x
    def type_determine(x: Any) -> Types | Any:
        return int_(bool_(str_(x)))

    return type_determine(x) if type_determine(x) != x else str_repr


# Haskell Generators
type HsTypes = Literal["String"] | Literal["Integer"] | Literal["Boolean"]
type HsTypeDef = str
# INFO:
# type HsDataDef = str
# def hsTypes(x: Any) -> HsTypes:
#     return type_determiner("String", "Boolean", "Integer", x) # type: ignore
# def hsTypeDef(f: Field) -> HsTypeDef:
#     return f"  {f.name} :: {hsTypes(f.type)}"
# def hsDataDef(t: Table) -> HsDataDef:
#     return (
#         f"{{- Definition constructed from {t.name} type in {__file__} -}}\n"
#         f"data {t.name} = {t.name}\n"
#         "  { \n"
#         f"    {join_to_comma(map(hsTypeDef, t.fields))}\n"
#         "  }\n\n"
#     )
# def hs_file_create(target_filename: FilePath, ts: List[Table]) -> IO:
#     with open(target_filename, "w") as f:
#         f.write(f"module DataDef( )where \n")
#         consume(map(f.write, map(hsDataDef, ts)))


# Elm Generators
type ElmTypes = Literal["String"] | Literal["Int"] | Literal["Bool"]
type ElmTypeDef = str
type ElmDataDef = str


def elmTypes(x: Any) -> ElmTypes:
    return type_determiner("String", "Bool", "Int", x) # type: ignore


def elmTypeDef(f: Field) -> ElmTypeDef:
    return f" {f.name} : {elmTypes(f.type)}"


def elmDataDef(t: Table) -> ElmDataDef:
    return (
        f"{{- Definition constructed from {t.name} type in {__file__} -}}\n"
        f"{t.name} : {{ {join_to_comma(map(elmTypeDef, t.fields))} }}"
        "\n\n"
    )


def elm_file_create(target_filename: FilePath, ts: List[Table]) -> IO:
    with open(target_filename, "w") as f:
        f.write("module DataDef where \n")
        consume(map(f.write, map(elmDataDef, ts)))


#
#
# MAIN
#
#
def main() -> IO:
    """
    Reinits database & updates the elm data definitions file for use on the frontend.
    """
    tables = list(map(lambda x: x.value, TABLES))

    os.remove(DB_NAME)

    cur: sql.Cursor = sql.connect(DB_NAME).cursor()
    scripts_table_create: list[SqlTable] = list(map(sqlTable, tables))
    consume(map(cur.executescript, scripts_table_create))
    cur.close()

    elm_file_create(ELM_NAME, tables)

if __name__ == "__main__":
    main()

