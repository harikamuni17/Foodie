from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.address import AddressCreate, AddressResponse
from app.models.address import Address
from app.dependencies.auth import get_current_customer

router = APIRouter(prefix="/api/v1/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressResponse)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_customer: int = Depends(get_current_customer)
):
    new_address = Address(customer_id=current_customer.id, **address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

@router.get("/", response_model=list[AddressResponse])
def get_addresses(
    db: Session = Depends(get_db),
    current_customer: int = Depends(get_current_customer)
):
    addresses = db.query(Address).filter(Address.customer_id == current_customer.id).all()
    return addresses

@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_customer: int = Depends(get_current_customer)
):
    address = db.query(Address).filter(Address.id == address_id, Address.customer_id == current_customer.id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_customer: int = Depends(get_current_customer)
):
    existing_address = db.query(Address).filter(Address.id == address_id, Address.customer_id == current_customer.id).first()
    if not existing_address:
        raise HTTPException(status_code=404, detail="Address not found")

    existing_address.street = address.street
    existing_address.city = address.city
    existing_address.state = address.state
    existing_address.zip_code = address.zip_code
    db.commit()
    db.refresh(existing_address)
    return existing_address

@router.delete("/{address_id}", response_model=AddressResponse)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_customer: int = Depends(get_current_customer)
):
    existing_address = db.query(Address).filter(Address.id == address_id, Address.customer_id == current_customer.id).first()
    if not existing_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(existing_address)
    db.commit()
    return existing_address

