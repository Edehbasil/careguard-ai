from fastapi import FastAPI

app = FastAPI(title="CareGuard AI")

@app.get("/")
def root():
    return {"message": "CareGuard AI backend is running"}
