import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from modules.visulaize_history import visulaize_history
from modules.build_model import build_model
from modules.preprocess_image import preprocess_image
from modules.data_generator import data_generator

with open('athletes_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

images = []
labels = []

for entry in data:
    img_path = entry['img']
    img_array = preprocess_image(img_path, (128,256))
    images.append(img_array)
    
    labels.append([
        1 if entry['species'] == 'person' else 0,
        float(entry['attack']),
        float(entry['defense']),
        float(entry['accuracy'].replace('%', '').strip()),
        float(entry['weight']),
        ])

X = np.array(images)
y = np.array(labels)

datagen = data_generator()

kfold = KFold(n_splits=5, shuffle=True)
fold_no = 1
all_histories = []

for train_index, test_index in kfold.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    train_datagen = datagen.flow(X_train, y_train, batch_size=16)

    athlete_model = build_model()

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    history = athlete_model.fit(
        train_datagen,
        steps_per_epoch=len(X_train) // 16,
        epochs=10,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping]
    )
    
    all_histories.append(history)
    athlete_model.save(f"M{fold_no}.keras")
    fold_no += 1


for i, history in enumerate(all_histories):
    visulaize_history(history, title=f"M{i + 1} Learning History")