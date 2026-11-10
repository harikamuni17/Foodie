
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.dependencies.auth import get_current_customer
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerLogin
from app.services.security import hash_password, verify_password, create_access_token

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

@router.post("/login")
def login_customer(
    customer: CustomerLogin,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if not existing_customer or not verify_password(customer.password, existing_customer.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(existing_customer.id)

    return {"access_token": access_token}

@router.get("/me", response_model=CustomerResponse)
def get_my_profile(
    current_customer: Customer = Depends(get_current_customer)
):
    return current_customer
