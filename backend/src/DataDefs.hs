module DataDef where 
{- Definition constructed from User type in C:\Users\ellis.coon\Documents\Code\undset\scripts\data_setup.py -}
data User = User
  { 
      id :: String,   name :: String,   email :: String,   password :: String
  }

{- Definition constructed from Thread type in C:\Users\ellis.coon\Documents\Code\undset\scripts\data_setup.py -}
data Thread = Thread
  { 
      id :: String,   name :: String,   creator_id :: String
  }

{- Definition constructed from ThreadMessage type in C:\Users\ellis.coon\Documents\Code\undset\scripts\data_setup.py -}
data ThreadMessage = ThreadMessage
  { 
      id :: String,   thread_id :: String,   user_id :: String,   content :: String
  }

