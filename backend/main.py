from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{get_end_point}")
def dynamic_get(get_end_point: str):
    return {"message": f"Hello from {get_end_point}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)