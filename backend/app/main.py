from fastapi import FastAPI
app = FastAPI(title="Foodie API")

@app.get("/")
def home():
    return {"Welcome to the Foodie API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
