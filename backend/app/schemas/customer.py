from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None

    class Config:
        orm_mode = True

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str