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

class Task(BaseModel):
    status:str
    datestart:str
    timestart :str
    location :str
    machine :str
    problem:str
    commenttxt:str
    solve:str
    timefinish:str



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


@app.post("/register")
def reguser(user:User):
    with dbconnection() as conn:
        with conn.cursor() as cur:
            queryCheck = "SELECT username FROM datauser WHERE username = %s "
            cur.execute(queryCheck,(user.username,))
            result = cur.fetchone()
            if result :
                raise HTTPException (status_code=400,detail="username already used")
            try :
                query= "INSERT INTO datauser(username,password) VALUES(%s,%s)"
                cur.execute(query,(user.username,user.password))
                conn.commit()
                return{"status":"success", "message":"register success"}
            except Exception as e :
                raise HTTPException(status_code=500, detail=str(e))
            
@app.get("/dataLine")
def getdataLine():
    with dbconnection() as conn:
        with conn.cursor() as cur :
            query= "SELECT * From productionline"
            cur.execute(query)
            result = cur.fetchall()
            result_list = [row[0] for row in result]
            return result_list

@app.get("/dataMachine")
def getdataLine():
    with dbconnection() as conn:
        with conn.cursor() as cur :
            query= "SELECT * From productionmachine"
            cur.execute(query)
            result = cur.fetchall()
            result_list = [row[0] for row in result]
            return result_list


@app.get("/dataProblem")
def getdataLine():
    with dbconnection() as conn:
        with conn.cursor() as cur :
            query= "SELECT * From productionproblem"
            cur.execute(query)
            result = cur.fetchall()
            result_list = [row[0] for row in result]
            return result_list

@app.post("/taskInput")
def sendTask(task:Task):
    with dbconnection() as conn:
        with conn.cursor() as cur:
            try:
                query = " INSERT INTO tasktable(status,timestart,location,machine,problem,comment,solve,timefinish) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(query,(task.status,task.timestart,task.location,task.machine,task.problem,task.commenttxt,task.solve,task.timefinish))
                conn.commit()
                return{"status":"success", "message":"send data success"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))



                




