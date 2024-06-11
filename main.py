import tkinter as tk
from audio_processing import load_and_play_audio_file, control_window
import pygame
from tensorflow.keras.models import load_model
import pickle
from prediction import analyze
import os
import sys
import resampy

# Инициализация Pygame
pygame.mixer.init()

# Определяем, запущено ли приложение из исполняемого файла
is_frozen = getattr(sys, 'frozen', False)

# Загрузка модели и весов
# Определяем путь к файлу mymodel.h5 в зависимости от того, запущено ли приложение из исходного кода или из исполняемого файла
if is_frozen:
    # Запущено из исполняемого файла, используем sys._MEIPASS
    model_path = os.path.join(sys._MEIPASS, 'mymodel.h5')
    weights_path = os.path.join(sys._MEIPASS, 'weights.h5')
    model = load_model(model_path)
    model.load_weights(weights_path)
    with open(os.path.join(sys._MEIPASS, './scaler.pkl'), 'rb') as file:
        loaded_scaler = pickle.load(file)
else:
    # Запущено из исходного кода, используем относительный путь
    model_path = './mymodel.h5'
    weights_path = './weights.h5'
    model = load_model(model_path)
    model.load_weights(weights_path)
    with open('./scaler.pkl', 'rb') as file:
        loaded_scaler = pickle.load(file)

disease = ['Бронхоэктатическая болезнь', 'Бронхиолит', 'Хроническая обструктивная болезнь легких (ХОБЛ)', 'Здоров', 'Пневмония', 'URTL']

# Глобальные переменные
global audio_file_path
audio_file_path = ""

# Функция для запуска приложения
def run_app():
    root = tk.Tk()
    root.title("RespPredict")

    # Определяем путь к иконке в зависимости от того, запущено ли приложение из исходного кода или из исполняемого файла
    if is_frozen:
    # Запущено из исполняемого файла, используем sys._MEIPASS
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
    # Запущено из исходного кода, используем относительный путь
        icon_path = './icon.ico'

    # Устанавливаем иконку для окна
    root.iconbitmap(icon_path)

    # root.iconbitmap(r'./icon.ico')

    left_frame = tk.Frame(root)
    right_frame = tk.Frame(root)

    left_frame.grid(row=0, column=0, sticky="nsew")
    right_frame.grid(row=0, column=1, sticky="nsew")

    buttons_frame = tk.Frame(left_frame)
    buttons_frame.pack(fill=tk.BOTH, expand=True)

    results_text = tk.Text(right_frame, wrap=tk.WORD, font=("Arial", 12), width=20, height=3)
    results_text.pack(fill=tk.BOTH, expand=True)

    def file():
        global audio_file_path
        audio_file_path = load_and_play_audio_file(play_button, predict_button)
        results_text.delete('1.0', tk.END)
        results_text.insert(tk.END, "Файл загружен\n")

    upload_button = tk.Button(buttons_frame, text="Загрузка аудиофайла", command=lambda: file(), width=24, height=5)
    upload_button.grid(row=0, column=0, sticky="ew")

    play_button = tk.Button(buttons_frame, text="Воспроизведение аудиофайла", state='disabled', command=lambda: control_window(play_button, root), width=24, height=5)
    play_button.grid(row=1, column=0, sticky="ew")

    predict_button = tk.Button(buttons_frame, text="Анализ и предсказание", state='disabled', width=24, height=5, command=lambda: analyze(results_text, audio_file_path, loaded_scaler, model, disease))
    predict_button.grid(row=2, column=0, sticky="ew")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.mainloop()

if __name__ == "__main__":
    run_app()