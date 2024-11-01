import onnxruntime as ort

def load_model(model_path: str):
    return ort.InferenceSession(model_path)