from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    #id : int // db에서 직접 id 할당
    contents : str
    is_done : bool

    
class SignUpRequest(BaseModel):
    username : str
    password : str

class LogInRequest(BaseModel):
    username : str
    password : str