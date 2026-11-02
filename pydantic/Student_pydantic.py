from pydantic import BaseModel  , EmailStr  , field_validator , Field ,model_validator , field_serializer
from typing import Optional , List

class student(BaseModel):
    name :str
    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.upper()
    age :int=Field(gt=0, lt=35)
    email:EmailStr
    subjects : List[str] = Field(min_length=3, max_length=10)
    contact : List[str] 
    Addres :Address_details

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

class Address_details(BaseModel):
    building_name :str
    street_name:str
    city:str
    state:str
    pincode:int=Field(gt=10000, lt=999999) 



def Insert_student(student1:student):
    print(student1.name)
    print(student1.age)
    print(student1.email)
    print(student1.subjects)
    print(student1.contact)
    print(student1.Addres.city)
    print(student1.Addres.pincode)
    print("Student data is inserted successfully")  

student1=student(name="Sahil", age = 19,email='sahi@atharvacoe.ac.in',subjects = ['pyhton','DBMS','adsa','ML','Dl'], contact=['personal:9876543210'] , Addres=Address_details(building_name='Maleshwar krupa chawl and socity', street_name='Nagindas pada', city='Mumbai', state='Maharashtra', pincode=401209))
# Insert_student(student1)
student_data = student1.model_dump(
    include={'name', 'age', 'email'}
)
print(student_data)
print(type(student_data))

