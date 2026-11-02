from pydantic import BaseModel  , EmailStr  , field_validator , Field ,model_validator
from typing import Optional , List

class student(BaseModel):
    name :str
    age :int=Field(gt=0, lt=35)
    email:EmailStr
    subjects : List[str]
    contact : List[str] 

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['atharvacoe.ac.in']
        input_domain = value.split("@")[-1]

        if input_domain not in valid_domains:
            raise ValueError('Email must be from atharvacoe.ac.in')
        return value

    @field_validator('subjects')
    @classmethod
    def subject_validator(cls,value):
        if len(value)<5:
            raise ValueError("Subject must be at least 5")
        return value

    @field_validator('name')
    @classmethod
    def name_validator(cls , value):
        if len(value)>50:
            raise ValueError("Name must be at most 50 characters")
        return value   
        
    @model_validator(mode='before')
    @classmethod
    def age_contact_validator(cls , values):
        age = values.get('age')
        contact = values.get('contact')

        if age <18 and not 'emergency' in contact:
            raise ValueError(" Emergenacy Contact information is required for students under 18")
        return values    


def Insert_student(student1:student):
    print(student1)
    print("Student data is inserted successfully")  

student1=student(name="Sahil", age = 17,email='sahi@atharvacoe.ac.in',subjects = ['pyhton','DBMS','adsa','ML','Dl'], contact=['personal:9876543210'])
Insert_student(student1)