import sqlite3
import bcrypt

# ---------------------------
# DB SETUP
# ---------------------------

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

conn.commit()

# ---------------------------
# HASH PASSWORD
# ---------------------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# ---------------------------
# VERIFY PASSWORD
# ---------------------------
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------------------
# ADD USER
# ---------------------------
def create_user(username, password):
    try:
        hashed = hash_password(password)
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except:
        return False

# ---------------------------
# LOGIN USER
# ---------------------------
def login_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if result:
        return verify_password(password, result[0])
    
    return False