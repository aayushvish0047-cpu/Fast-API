import json
from pathlib import Path as FilePath
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator


class Patient(BaseModel):
    id: Annotated[str, Field(min_length=1, description="The ID of the patient")]
    name: Annotated[str, Field(min_length=1, description="The name of the patient")]
    age: Annotated[int, Field(ge=0, le=130, description="The age of the patient")]
    height: Annotated[
        float, Field(ge=50, le=250, description="The patient's height in centimeters")
    ]
    weight: Annotated[
        float, Field(ge=2, le=500, description="The patient's weight in kilograms")
    ]
    gender: Annotated[str, Field(min_length=1, description="The gender of the patient")]
    city: Annotated[str, Field(min_length=1, description="The city of the patient")]
    condition: Annotated[
        list[str], Field(min_length=1, description="The patient's medical conditions")
    ]

    @field_validator("condition")
    @classmethod
    def validate_conditions(cls, conditions: list[str]) -> list[str]:
        normalized_conditions = [condition.strip() for condition in conditions]
        if any(not condition for condition in normalized_conditions):
            raise ValueError("Conditions must not be empty")
        return normalized_conditions

    @model_validator(mode="after")
    def validate_body_measurements(self) -> "Patient":
        if not 10 <= self.bmi <= 80:
            raise ValueError("BMI computed from height and weight must be between 10 and 80")
        return self

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height / 100) ** 2, 2)


app = FastAPI()


def load_data() -> list[Patient]:
    with open(FilePath(__file__).with_name("patients.json"), encoding="utf-8") as file:
        data = json.load(file)
    return [Patient.model_validate(patient) for patient in data]


def save_data(data: list[Patient]) -> None:
    patients_path = FilePath(__file__).with_name("patients.json")
    with patients_path.open("w", encoding="utf-8") as file:
        json.dump(
            [patient.model_dump(exclude={"bmi"}) for patient in data],
            file,
            indent=2,
        )

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

@app.get("/view", response_model=list[Patient])
def view():
    return [patient.model_dump() for patient in load_data()]


@app.get("/patient/{patient_id}", response_model=Patient)
def view_patient(
    patient_id: str = Path(..., description="The ID of the patient to retrieve", examples=["P001"])
):
    data = load_data()
    patient = next((patient for patient in data if patient.id == patient_id), None)
    if patient is not None:
        return patient.model_dump()
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")


@app.get("/sort", response_model=list[Patient])
def sort_patients(
    sort_by: str = Query(..., description="The field to sort patients by"),
    order: str = Query(
        "asc", description="The order of sorting: 'asc' for ascending, 'desc' for descending"
    ),
):
    data = [patient.model_dump() for patient in load_data()]
    if sort_by not in Patient.model_fields and sort_by not in Patient.model_computed_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid order: {order}. Must be 'asc' or 'desc'.")

    sort_order = order == "desc"
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=sort_order)
    return sorted_data

@app.post("/create", response_model=Patient, status_code=201)
def create_patient(patient: Patient):
    data = load_data()
    if any(existing_patient.id == patient.id for existing_patient in data):
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists")
    data.append(patient)
    save_data(data)
    return patient