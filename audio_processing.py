import pygame
import tkinter as tk
from tkinter import filedialog, messagebox

# Инициализация Pygame
pygame.mixer.init()

audio_loaded = False

def load_and_play_audio_file(play_button, predict_button):
    global audio_loaded, audio_file_path

    audio_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav"), ("All Files", "*.*")])
    if audio_file_path:
        try:
            pygame.mixer.music.load(audio_file_path)
            audio_loaded = True
            play_button.config(state='normal')
            predict_button.config(state='normal')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки аудиофайла: {str(e)}")
    return audio_file_path

def control_window(play_button, root):   
    if audio_loaded:
        def pause_audio_file():
            pygame.mixer.music.pause()
            pause_button.config(state='disabled')
            resume_button.config(state='normal')

        def resume_audio_file():
            pygame.mixer.music.unpause()
            resume_button.config(state='disabled')
            pause_button.config(state='normal')    

        def stop_audio_file():
            pygame.mixer.music.stop()
            resume_button.config(state='normal')
            pause_button.config(state='normal')    

        def play_audio_file():
            global audio_loaded
            if audio_loaded:
                pygame.mixer.music.play()
                root.after(100, update_status)
                resume_button.config(state='normal')
                pause_button.config(state='normal')  

        def update_status():
            global audio_loaded
            if pygame.mixer.music.get_busy():
                pass  # Здесь можно добавить код для обновления интерфейса
            else:
                audio_loaded = False  # Сбрасываем флаг после завершения воспроизведения

        control_window = tk.Toplevel(root)
        control_window.title("Audio Control")
        control_window.geometry('190x160')

        play_button = tk.Button(control_window, text="Play", command=play_audio_file)
        play_button.pack(side=tk.TOP, padx=10, pady=5)
        
        pause_button = tk.Button(control_window, text="Pause", state='disabled', command=pause_audio_file)
        pause_button.pack(side=tk.TOP, padx=10, pady=5)

        resume_button = tk.Button(control_window, text="Resume", state='disabled', command=resume_audio_file)
        resume_button.pack(side=tk.TOP, padx=10, pady=5)
        
        stop_button = tk.Button(control_window, text="Stop", command=stop_audio_file)
        stop_button.pack(side=tk.TOP, padx=10, pady=5)

        # control_window.protocol("WM_DELETE_WINDOW", close_control_window())

