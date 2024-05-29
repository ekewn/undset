import os
import sqlite3
from enum import Enum
from typing import Any, Callable, Literal, NamedTuple

#
#
# DATA
#
#

# Consts
DB_NAME = f"backend{os.pathsep}db.db"

# Type Aliases
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
type HsType = Literal["Integer"] | Literal["Integer"] | Literal["Boolean"]
type HsTypeDef = str

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
# SQL Generators
def table_create_sql(t: TABLES) -> Sql:
    field_sql: map[Sql] = map(field_create_sql, t.value.fields)
    any_foreign_keys: bool = any(list(map(lambda f: f.is_foreign_key, t.value.fields))) 
    foreign_keys: list[Name] = list(
        map(lambda f: f.name, 
            filter(lambda f: f.is_foreign_key, t.value.fields)))

    return ( 
        f" CREATE TABLE IF NOT EXISTS {t.name} ( "
        f" {", ".join(list(field_sql))} "
        f" {", " + ", ".join(list(map(foreign_key_create_sql, foreign_keys))) if any_foreign_keys else ''}"
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
hs_int: Any = lambda _: "Integer" if isinstance(_, int) else _
hs_str: Any = lambda _: "String" if isinstance(_, str) else _
hs_bool: Any = lambda _: "Boolean" if isinstance(_, bool) else _
hs_type: Callable[[Any], HsType] = lambda _: hs_int(hs_str(hs_bool(_)))
hs_print_type: Callable[[Field], HsTypeDef] = lambda _: f"  {_.name} :: {hs_type(_.type)},"

def hs_create_defs(t: TABLES) -> Succeeded:
    file_name: FilePath = f"{os.getcwd()}{os.pathsep}backend{os.pathsep}src{os.pathsep}data.hs"
    try:
        with open(file_name, "w") as f:
            f.write("{- Data Generated from data_setup.py -}")
            f.write(f"data {t.value.name} = {t.value.name} {{")
            f.write("  {")
            list(map(f.write, map(hs_print_type, t.value.fields)))
            f.write("  }")
            f.write("")
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
    list(map(hs_create_defs, TABLES))

