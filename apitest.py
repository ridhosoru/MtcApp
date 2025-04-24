from fastapi import FastAPI


app = FastAPI()


@app.post("/tes")
def root():
    return{"hello":"world"}
    