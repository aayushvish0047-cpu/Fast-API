from fastapi import FastAPI ,Path , HTTPException , Query
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
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data =  load_data()

    if patient_id  in[ patient['id'] for patient in data] :
        return next(patient for patient in data if patient["id"] == patient_id)
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
      
@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description="The field to sort patients by"), order:str=Query('asc',description="The order of sorting: 'asc' for ascending, 'desc' for descending")):
    data = load_data()
    if sort_by not in data[0]:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order: {order}. Must be 'asc' or 'desc'.")    

    sort_order = True if order =='desc' else False
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=sort_order)
    return sorted_data
