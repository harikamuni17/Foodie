from fastapi import FastAPI
from app.database import Base, engine
from app.models.customer import Customer
from app.models.address import Address
from app.routes.customer import router as customer_router
from app.routes.address import router as address_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Foodie API")

app.include_router(customer_router)
app.include_router(address_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Foodie API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-health")
def db_health():
    try:
        from app.database import test_db
        test_db()
        return {"status": "healthy"}
    except Exception:
        return {"status": "unhealthy"}
