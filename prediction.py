import tkinter as tk
from feature_extraction import prepare
import numpy as np

def predict_on_batch(batched_input, model):
    return model(batched_input)

def analyze(results_text, audio_file_path, loaded_scaler, model, disease):
    results_text.delete('1.0', tk.END)

    # Проверяем, загружен ли аудиофайл
    if not audio_file_path:
        print("Аудиофайл не загружен.")
        return  # Прекращаем выполнение функции
    
    flattened_features = prepare(audio_file_path, loaded_scaler)
    
    # Используйте функцию predict_on_batch для предсказания
    predictions = predict_on_batch(flattened_features, model)
    predicted_class = np.argmax(predictions, axis=1)

    # После извлечения признаков
    if flattened_features is None:
        results_text.insert(tk.END, f"Не удалось обработать файл: {audio_file_path}\n")
    else:
        # Продолжаем предсказание
        predictions = predict_on_batch(flattened_features, model)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_disease = [disease[i] for i in predicted_class]
        results_text.insert(tk.END, f"Прогнозируемое заболевание: {predicted_disease[2]}\n")