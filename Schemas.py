from pydantic import BaseModel


class BroadcastSchema(BaseModel):
    text: str

class UserCreate(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
