import sqlite3
from enum import Enum
from typing import Literal, NamedTuple

#
#
# DATA
#
#

# Consts
DB_NAME = "db.db"

# Type Aliases
type Id = int
type Name = str
type Email = str
type Password = str
type Content = str
type Sql = str
type TableFields = list[Field]
type FieldType = Literal["INTEGER"] | Literal["TEXT"]
type FieldIsPrimaryKey = bool
type FieldIsForeignKey = bool
type FieldIsNullable = bool
type FieldIsUnique = bool
type ThreadCreatorId = int

# Types
Table = NamedTuple("Table" , [("name", Name) , ("fields", TableFields)])
Field = NamedTuple("Field",
                   [("name", Name)
                   , ("type", FieldType)
                   , ("isPrimaryKey", FieldIsPrimaryKey)
                   , ("isForeignKey", FieldIsForeignKey)
                   , ("isNullable", FieldIsNullable)
                   , ("isUnique", FieldIsUnique)])
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

# TODO: Test Data

#
#
# FUNCTIONS
#
#
def table_create_sql(t: TABLES) -> Sql:
    field_sql: map[Sql] = map(field_create_sql, t.value.fields)
    any_foreign_keys: bool = any(list(map(lambda f: f.isForeignKey, t.value.fields))) 
    foreign_keys: list[Name] = list(
        map(lambda f: f.name, 
            filter(lambda f: f.isForeignKey, t.value.fields)))

    return ( 
        f" CREATE TABLE IF NOT EXISTS {t.name} ( "
        f" {", ".join(list(field_sql))} "
        f" {", " + ", ".join(list(map(foreign_key_create_sql, foreign_keys))) if any_foreign_keys else ''}"
        ");")


def foreign_key_create_sql(f_name: Name) -> Sql:
    t_name: Name = f_name.split("_")[0]
    return f" FOREIGN KEY ({f_name}) REFERENCES {t_name.title()} (id) "


def field_create_sql(f: Field) -> Sql:
    is_primary_key: str = "PRIMARY KEY" if f.isPrimaryKey else ""
    is_unique: str = "UNIQUE" if f.isUnique else ""
    is_nullable : str = "" if f.isNullable else "NOT NULL"
    return f"{f.name} {f.type} {is_primary_key} {is_nullable} {is_unique} "


#
#
# MAIN
#
#
if __name__ == "__main__":
    cur = sqlite3.connect(DB_NAME).cursor()
    scripts_table_create = list(map(table_create_sql, TABLES))
    list(map(cur.executescript, scripts_table_create))

