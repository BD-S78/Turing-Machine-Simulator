from fastapi import FastAPI, HTTPException
from simulator import simulate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
app = FastAPI()

MONGODB_URL = os.getenv("MONGODB_URL")


client = AsyncIOMotorClient(MONGODB_URL)
db = client.turing_machine_db
machines_collection = db.machines



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://turing-machine-simulator.onrender.com/"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationInput(BaseModel):
    machinecode: str
    problemcode: list[str]

class SavedMachine(BaseModel):
    name: str
    machineCode: str
    description: str = "" #Optional

@app.get("/")
def root():
    return {"message": "Welcome to Local AI-enabled Restaurant API"}


@app.post("/run-tm")
async def run_tm_simulation(item: SimulationInput):
    try:
        results = simulate(item.machinecode, item.problemcode)
        #send the results to frontend
        return {"status": "finished", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@app.get("/test-db")
async def test_db():
    try:
        # This sends a "ping" to the database to see if it responds
        await client.admin.command('ping')
        return {"status": "success", "message": "Connected to MongoDB!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.post("/save-tm-db")
async def save_tm_db(machine: SavedMachine):
    try:
        new_machine = machine.model_dump()

        #timestamp
        new_machine["createdAt"] = datetime.now(timezone.utc)
        
        # Insert into MongoDB
        result = await machines_collection.insert_one(new_machine)
        
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save to database") from e
    

@app.get("/get-tms")
async def get_tms():
    try:
        machines = []
        #Look through db and find previous saved
        #simple just 20 most recent created ones because the main thing is to make your own.
        mostRecent = machines_collection.find().sort("createdAt", -1).limit(20)

        async for tm in mostRecent:
            machines.append({
                "id": str(tm.get("_id")),
                "name": tm.get("name"),
                "machineCode": tm.get("machineCode"),
                "description": tm.get("description", "")
            })
        return machines
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e