
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.security import hash_password

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)

@router.post("/register", response_model=CustomerResponse)
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        password_hash=hash_password(customer.password),
        phone=customer.phone
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer
