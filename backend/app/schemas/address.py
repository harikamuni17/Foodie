from pydantic import BaseModel

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    label: str

class AddressResponse(BaseModel):
    id: int
    customer_id: int
    street: str
    city: str
    state: str
    zip_code: str
    label: str

    class Config:
        orm_mode = True 