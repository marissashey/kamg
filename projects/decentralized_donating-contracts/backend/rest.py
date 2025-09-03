from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.post("/contract/interact")
def interact_contract(data: dict):
    # TODO: Add logic to interact with Algorand smart contracts
    return {"status": "success"}
