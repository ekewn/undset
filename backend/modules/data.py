import os
from typing import List, Literal, NamedTuple


#
#
# DATA
#
#

# Domain Types
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
