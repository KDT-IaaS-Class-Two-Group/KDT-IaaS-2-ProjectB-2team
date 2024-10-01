from fastapi import FastAPI, UploadFile, File, HTTPException
from modules.model_loader import load_model
from modules.FastAPI_preprocess import model_predict  # model_predict 함수를 import
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

# 학습된 모델을 앱 시작 시 한 번만 로드
model = load_model("./model/M5.keras")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # model_predict 함수를 호출하여 예측 결과를 가져옴
        response = await model_predict(file, model)
        print(response)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
