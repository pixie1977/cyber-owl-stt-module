"""
Конфигурационный файл приложения STT.
Загружает переменные окружения и устанавливает значения по умолчанию.
"""

import os
from distutils.util import strtobool
from dotenv import load_dotenv


# Определяем текущую директорию
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Загружаем .env файл
load_dotenv()


# Проверка обязательной переменной
STT_USE_TORCH_MODEL_MANAGER_STR = os.getenv("STT_USE_TORCH_MODEL_MANAGER_STR")
if not STT_USE_TORCH_MODEL_MANAGER_STR:
    raise ValueError("Не задан STT_USE_TORCH_MODEL_MANAGER_STR в .env")

STT_USE_TORCH_MODEL_MANAGER = strtobool(STT_USE_TORCH_MODEL_MANAGER_STR)


# Аудиоустройство
STT_SOUND_DEVICE_INDEX = os.getenv("STT_SOUND_DEVICE_INDEX")
if not STT_SOUND_DEVICE_INDEX:
    raise ValueError("Не задан STT_SOUND_DEVICE_INDEX в .env")

STT_SOUND_DEVICE_INDEX = int(STT_SOUND_DEVICE_INDEX)

# Пути к моделям
STT_VOSK_MODEL_PATH = os.getenv("STT_VOSK_MODEL_PATH")
if not STT_VOSK_MODEL_PATH:
    STT_VOSK_MODEL_PATH = os.path.join(CURRENT_DIRECTORY, "..", "models", "vosk-model-small-ru-0.22")

STT_SPK_MODEL_PATH = os.getenv("STT_SPK_MODEL_PATH")
if not STT_SPK_MODEL_PATH:
    STT_SPK_MODEL_PATH = os.path.join(CURRENT_DIRECTORY, "..", "models", "vosk-model-spk-0.4")


# Путь к примерам голосов
STT_SAMPLE_VOICES_PATH = os.getenv("STT_SAMPLE_VOICES_PATH")
if not STT_SAMPLE_VOICES_PATH:
    STT_SAMPLE_VOICES_PATH = os.path.join(CURRENT_DIRECTORY, "..", "resources", "sample_voices")


# Путь к статическим файлам (HTML, JS)
STT_DOC_ROOT = os.getenv("STT_DOC_ROOT")
if not STT_DOC_ROOT:
    STT_DOC_ROOT = os.path.join(CURRENT_DIRECTORY, "..", "content")


# Настройки сервера
STT_PORT = os.getenv("STT_PORT")
if not STT_PORT:
    raise ValueError("Не задан STT_PORT в .env")
STT_PORT = int(STT_PORT)

STT_HOST = os.getenv("STT_HOST")
if not STT_HOST:
    raise ValueError("Не задан STT_HOST в .env")

STT_LOG_LEVEL = os.getenv("STT_LOG_LEVEL")
if not STT_LOG_LEVEL:
    raise ValueError("Не задан STT_LOG_LEVEL в .env")

STT_URL_TO_TEXT_TRANSMIT = os.getenv("STT_URL_TO_TEXT_TRANSMIT")

STT_LOGS_DIR = os.getenv("STT_LOGS_DIR")
