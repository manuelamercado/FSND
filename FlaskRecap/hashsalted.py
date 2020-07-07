# Import the Python Library
import sys
!{sys.executable} -m pip install bcrypt
import bcrypt

password = b"studyhard"

 # Hash a password for the first time, with a certain number of rounds
salt = bcrypt.gensalt(14)
hashed = bcrypt.hashpw(password, salt)
print(salt)
print(hashed)

bcrypt.checkpw(password, hashed)

hashed = b'$2b$14$EFOxm3q8UWH8ZzK1h.WTZeRcPyr8/X0vRfuL3/e9z7AKIMnocurBG'
password = b"learningisfun"
bcrypt.checkpw(password, hashed)
