from pydantic import BaseModel ,EmailStr
from typing import Optional

class student(BaseModel):
    name :str
    age : Optional[int] = None
    email: EmailStr

def Insert_student(student1:student):
    print(student1.name)
    print(student1.age)
    print(student1.email)

    print("Student data inserted successfully")

student1 = student(name="Karan", email="karan@google.com")
student2 =  student(name="Aayush",age = 19, email='aayushvishwakakarma-inft@athrvacoe.ac.in')
Insert_student(student1)
Insert_student(student2)
