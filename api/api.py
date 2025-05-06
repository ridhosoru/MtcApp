from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import psycopg2
from typing import Optional


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
    status:Optional[str] = None
    datestart:Optional[str] = None
    timestart :Optional[str] = None
    timerespon:Optional[str] = None
    location :Optional[str] = None
    machine :Optional[str] = None
    problem:Optional[str] = None
    commenttxt:Optional[str] = None
    problemaftercheck:Optional[str] = None
    solve:Optional[str] = None
    timefinish:Optional[str] = None
    namemtc:Optional[str] = None

class getDate(BaseModel):
    datestart : Optional[str] = None



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
                query = " INSERT INTO tasktable(status,datestart,timestart,timerespon,location,machine,problem,comment,problemafter_check,solve,timefinish,namemtc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(query,(task.status,task.datestart,task.timestart,task.timerespon,task.location,
                            task.machine,task.problem,task.commenttxt,task.problemaftercheck,task.solve,task.timefinish,task.namemtc))
                conn.commit()
                return{"status":"success", "message":"send data success"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.get("/getTask")
def getTask():
    with dbconnection() as conn:
        with conn.cursor() as cur :
            try:
                query="SELECT * FROM tasktable"
                cur.execute(query)
                result= cur.fetchall()
                return result
            except Exception as e :
                raise HTTPException(status_code=500, detail=str(e))
            
@app.get("/getstatusR")
def getstatusR():
    with dbconnection() as conn :
        with conn.cursor() as cur :
            query = "SELECT status from tasktable "
            cur.execute(query)
            result = cur.fetchall()
            status_list = [row[0] for row in result]
            return {"status": "success", "data": status_list}

@app.post("/closetask")    
def closetaskR(task:Task):
    with dbconnection() as conn :
        with conn.cursor() as cur :
            try:
                query = "UPDATE tasktable SET status = %s,problemafter_check=%s,solve=%s,timefinish=%s,namemtc=%s WHERE " \
                "datestart=%s AND timestart=%s AND timerespon=%s AND location=%s AND machine=%s AND problem=%s AND comment=%s "
                cur.execute(query,(task.status,task.problemaftercheck,task.solve,task.timefinish,task.namemtc,task.datestart,task.timestart,task.timerespon,task.location,
                                task.machine,task.problem,task.commenttxt))
                conn.commit()
                return {"status":"success", "message":"send data success"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))   

@app.post("/updaterespon")
def updateRespon(task:Task):
    with dbconnection() as conn :
        with conn.cursor() as cur :
            try:
                query = "UPDATE tasktable SET status = %s,timerespon=%s WHERE " \
                "datestart=%s AND timestart=%s AND location=%s AND machine=%s AND problem=%s AND comment=%s AND problemafter_check=%s AND solve=%s AND timefinish=%s AND namemtc=%s"
                cur.execute(query,(task.status,task.timerespon,task.datestart,task.timestart,task.location,
                                task.machine,task.problem,task.commenttxt,task.problemaftercheck,task.solve,task.timefinish,task.namemtc))
                conn.commit()
                return {"status":"success", "message":"send data success"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.post("/getDataWDate")
def getDataWDate(getdate:getDate):
    with dbconnection() as conn :
        with conn.cursor() as cur :
            try:
                query ="SELECT * from tasktable WHERE datestart=%s"
                cur.execute(query,(getdate.datestart,))
                result = cur.fetchall()
                return result
                
            except Exception as e:
                raise HTTPException(status_code=500,detail=str(e))




