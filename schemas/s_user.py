from pydantic import BaseModel, EmailStr


class RUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class LUser(BaseModel):
    email: EmailStr
    password: str