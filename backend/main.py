from fastapi import FastAPI ,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from modules.FastAPI_preprocess import model_predict
from modules.load_model import load_model
import uvicorn
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data', 'data.json')

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # JSON 파일을 파싱해서 Python 객체로 변환




@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{get_end_point}")
def dynamic_get(get_end_point: str):
    return {"message": f"Hello from {get_end_point}"}



model = load_model("./model/M5.keras")

@app.post("/predict")
async def predict_response(file: UploadFile = File(...)):
    print("test")
    result = await model_predict(file,model)
    return result
        
    

@app.post("/{post_end_point}")
def dynamic_get(post_end_point: str):
    return {"message",data}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)