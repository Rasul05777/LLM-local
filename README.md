# Запуск на Linux 

# 1. Клонируйте репозиторий и перейдите в каталог
cd /ваш/путь/к проекту

# 2. Разрешите контейнерам выводить окна на ваш X-сервер (один раз)
xhost +local:docker

# 3. Запустите стэк (первый раз скачивается образ Ollama и модель 4-5 ГБ)
docker compose up --build


Что произойдет при запуске:
1. Контейнер `ollama` запускает `ollama serve`, затем автоматически выполняет `ollama pull llama3.1:8b-instruct-q4_K_M`. Модель сохраняется во внешнем томе `ollama_data`.
2. Health-check (`ollama list`) подтверждает готовность сервера и модели.
3. Контейнер `app` (Python 3.11 + Tkinter) запускает `python main.py` и показывает окно.

Повторные запуски используют уже скачанную модель и стартуют быстрее.

# Запуск в Windows

На Windows нет встроенного X-сервера, поэтому есть два варианта:

1. Использовать внешний X-сервер (VcXsrv / Xming / X410) и запускать GUI из контейнера.
   ```powershell
   # установите и запустите VcXsrv (дисплей :0)
   $Env:DISPLAY="host.docker.internal:0.0"
   docker compose up --build
   ```
   Контейнер `app` возьмёт переменную `DISPLAY` и выведет окно в VcXsrv. Команда `xhost` НЕ нужна.

2. Запускать GUI-приложение локально, а в Docker оставлять только Ollama.
   ```powershell
   docker compose up ollama       # стартует только сервис модели
   python -m venv .venv && .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py                 # GUI на вашей Windows
   ```
   В этом случае убедитесь, что переменная окружения `OLLAMA_API_URL` указывает на `http://localhost:11434` (по умолчанию так и есть).
