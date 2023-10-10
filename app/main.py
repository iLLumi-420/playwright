from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import duckdb

conn = duckdb.connect('./database/db.duckdb')

conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             name VARCHAR,
             username VARCHAR UNIQUE
    )
""")


class User(BaseModel):
    id: int
    name: str
    username: str

app = FastAPI()


@app.get('/')
def hello_world():
    return {"hello": "world"}

@app.post('/users/', response_model=User)
def create_user(user: User):
    user_data = user.dict()
    conn.execute("INSERT INTO users (id, name, username) VALUES (?, ?, ?)", (user_data['id'], user_data['name'], user_data['username']))
    conn.commit()

    result = conn.execute(f"SELECT * from users WHERE id=?",(user_data['id'],)).fetchone()

    return {
        'id': result[0],
        'name': result[1],
        'username': result[2]
    }

@app.get('/users/', response_model=List[User])
def get_all_users():
    results = conn.execute("SELECT * from users").fetchall()
    return [{
        'id': result[0],
        'name': result[1],
        'username': result[2]
    } for result in results]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        'id': result[0],
        'name': result[1],
        'username': result[2],
    }

@app.put('/users/{user_id}', response_model=User)
def update_user(user: User):
    user_data = user.dict()
    conn.execute("UPDATE users SET name = ?, username = ? WHERE id = ?", (user_data['name'], user_data['username'], user_data['id']))
    
    if conn.total_changes == 0:
        raise HTTPException(status_code=404, detail="User not found")

    conn.commit()

    result = conn.execute("SELECT * FROM users WHERE id = ?", (user_data['id'],)).fetchone()
    
    return {
        'id': result[0],
        'name': result[1],
        'username': result[2],
    }

@app.delete('/users/{user_id}', response_model=User)
def delete_user(user_id: int):
    result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_return = {
        'id': result[0],
        'name': result[1],
        'username': result[2]
    }
    
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()

    return user_to_return



