import tensorflow as tf
import tf2onnx

# TensorFlow 모델 로드
model = tf.keras.models.load_model('./models/M5.keras')

# 모델을 ONNX로 변환
onnx_model, _ = tf2onnx.convert.from_keras(model)

# ONNX 모델 저장
with open("model_path.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
