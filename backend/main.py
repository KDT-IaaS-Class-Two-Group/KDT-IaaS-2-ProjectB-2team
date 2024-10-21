from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from typing import Dict, List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import base64
from modules.PPO_loader import run_simulation
from modules.adjust_populate import preprocess_population_density
from modules.model_loader import load_model
from modules.Image_model_predict import model_predict




app = FastAPI()




# CORS 설정    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("./modules/model/M5.keras")

class TempData:
    def __init__(self, nickname: str, region: str, img_data: bytes):
        self.nickname = nickname
        self.region = region
        self.img_data = img_data
        
async def M2(nickname: str, predictions: Dict[str, int], temp_array_1: List, temp_array_2: List) -> Dict:
    result = {
        "nickname": nickname,
        "stat": predictions,  # M1 모델의 예측 결과
        "log": [temp_array_1, temp_array_2]  # 두 개의 임시 배열
    }
    print("M2 함수 호출 결과:", result)
    return result

temp_storage = {}

@app.post("/result")
async def upload_and_predict(
    nickname: str = Form(...),
    region: str = Form(...),
    img: UploadFile = File(...)
):
    try:
        img_data = await img.read()

        temp_obj = TempData(nickname=nickname, region=region, img_data=img_data)
        temp_storage[nickname] = temp_obj  # nickname을 키로 사용하여 저장
        img_predict = await model_predict(temp_obj.img_data, model)
        simulate = await run_simulation(
            preprocess_population_density(region),
            img_predict)

        img_trans =  base64.b64encode(temp_obj.img_data).decode("utf-8")
        
        final_result = {
            "result": {
                "nickname": temp_obj.nickname,
                "img": img_trans,
                "region": temp_obj.region,
                "stat": img_predict,
                "log": simulate
            }
        }

        print(final_result)
        return final_result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction and result processing failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)