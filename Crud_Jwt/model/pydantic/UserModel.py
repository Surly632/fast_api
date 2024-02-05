from pydantic import BaseModel

class UserModel(BaseModel):
    first_name:str
    last_name:str
    username:str
    email:str
    password:str
    