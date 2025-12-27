from fastapi import FastAPI
from simulator import simulate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any "origin" to access the API for now
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationInput(BaseModel):
    machinecode: str
    problemcode: list[str]


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