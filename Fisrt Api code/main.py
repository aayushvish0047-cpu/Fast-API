from fastapi import FastAPI
import json
app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return {
        "message":"Patient Mangement system API"
    }
@app.get("/about")
def about():
    return {
        'message':' A fully functional API to manage patient records'
    }    

@app.get("/view")
def view():
    return load_data()