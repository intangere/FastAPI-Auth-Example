# FastAPI-Auth-Example

First clone the repository as usual:
```
git clone https://github.com/intangere/FastAPI-Auth-Example.git
```

Put it in a directory and then add a parent directory.
For example:
```
- > Auth_Parent
  - > Auth_Example
    - > <unpacked repo here>
```

Second edit config.py and set the following values
```
DATABASE_URL = 'sqlite:///./users.db' #Sqlite3 relative db url
MIN_PASSWORD_LEN = 8 #Minimum password length
USE_MSGPACK = False #Use msgpack over json if you prefer (experimental)
BRANCA_SECRET = '' #32 byte secret key (could be regenerated each time)
BRANCA_TTL = 3600 #How long do you want the user to stay logged in for

```
Then from the parent directory you can run the app with something like:
```
uvicorn app:app --host "0.0.0.0" --port 8080
```

The database should automatically be created when the app is ran.

**Brief Overview**
* Login/register model: POST with username/password pair
* Password hashing: Bcrypt for server-side password hashing
* Authentication: Branca token via *Authorization* header
* Request/Response format: JSON or Msgpack
* Type/data validation using Pydantic
