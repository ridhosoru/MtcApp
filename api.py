from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import psycopg2


app = FastAPI()

def dbconnection():
    return psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="101077",
                        port="5432")

class User(BaseModel):
    username : str
    password : str

@app.post("/login")
def loginapi(user:User):
    with dbconnection() as conn :
        with conn.cursor() as cur:
            query = "SELECT username, password FROM datauser WHERE username = %s AND password = %s"
            cur.execute(query, (user.username,user.password))
            result =cur.fetchone()
            if result :
                return {"status": "success", "message": "Login success"}
            raise HTTPException (status_code=401, detail="Invalid username or password")


# @app.post("reg")
# def registerapi(user:User):