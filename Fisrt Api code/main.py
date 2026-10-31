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
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str):
    data =  load_data()

    if patient_id  in[ patient['id'] for patient in data] :
        return next(patient for patient in data if patient["id"] == patient_id)
    else :    
        return
        {
            'message':'Patient not found'
        }    
