from pydantic import BaseModel,StrictFloat,EmailStr,Field

class Ticket(BaseModel):
     name:str
     amount:StrictFloat = Field(gt=0)
     isTrue:bool
     email:EmailStr
try:
     t = Ticket(name = "sowmya",amount = -50, isTrue = True, email ="email@email.com")
     print(t.amount)
except Exception as e:
     print("validation failed")
     print(e)
   
     
     