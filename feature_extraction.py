import librosa
import numpy as np
from tkinter import messagebox
import resampy


def add_noise(data):
    noise_value = 0.015 * np.random.uniform() * np.amax(data)
    data = data + noise_value * np.random.normal(size=data.shape[0])
    return data

def stretch_process(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate=0.8)

def pitch_process(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sr=sampling_rate, n_steps=pitch_factor)

def extract_process(data, sample_rate):
    output_result = np.array([])

    mean_zero = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    output_result = np.hstack((output_result, mean_zero))

    stft_out = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft_out, sr=sample_rate).T, axis=0)
    output_result = np.hstack((output_result, chroma_stft))

    mfcc_out = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=40).T, axis=0)
    output_result = np.hstack((output_result, mfcc_out))

    root_mean_out = np.mean(librosa.feature.rms(y=data).T, axis=0)
    output_result = np.hstack((output_result, root_mean_out))

    mel_spectogram = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    output_result = np.hstack((output_result, mel_spectogram))

    return output_result


def extract_features(file_name):
    """
    Эта функция принимает путь к аудиофайлу в виде строки, 
    загружает его и извлекает несколько аудиоатрибутов, 
    включая средние значения MFCC, нулевые переходы, хромограмму, 
    корневую среднеквадратичную энергию и мел-спектрограмму как от 
    ригинальной версии, так и от ее увеличенных вариантов.
    """
    try:
        # Load the original audio file
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast', duration=None, offset=0)

        # Extract features from the original audio data
        extracted_features = extract_process(audio, sample_rate)
        result = np.array(extracted_features)

        # Add noise and extract features
        noise_out = add_noise(audio)
        output_2 = extract_process(noise_out, sample_rate)
        result = np.vstack((result, output_2))

        # Time-stretch and then pitch-shift before extracting features
        new_out = stretch_process(audio,0.8)
        stretch_pitch = pitch_process(new_out, sample_rate,pitch_factor=0.7)
        output_3 = extract_process(stretch_pitch, sample_rate)
        result = np.vstack((result, output_3))
        result.shape

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка обработки аудиофайла: {str(e)}")
        return None

    return result

def prepare(audio_file_path, loaded_scaler):
    features = []
    global flattened_features
    data = extract_features(audio_file_path)
    features.append(data)
    features = np.array(features)
    flattened_features = features.reshape(-1, 182)
    flattened_features = loaded_scaler.transform(flattened_features)
    flattened_features = np.expand_dims(flattened_features,axis=2)
    return flattened_features