"""
Точка входа в приложение STT (Speech-to-Text).
Запускает сервер и фоновое прослушивание микрофона.
"""

import asyncio
import uvicorn

from app.core.httpd import app, stt_engine, message_queue
from app.config.config import STT_HOST, STT_PORT, STT_LOG_LEVEL
from app.utils.stt_utils import start_listening, set_event_loop, text_callback

if __name__ == "__main__":
    # Устанавливаем цикл событий
    # (иначе будут проблемы при запуске асинхронки в потоках)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    set_event_loop(loop)

    # Запускаем прослушивание
    start_listening(stt_engine, message_queue, text_callback)

    # Запускаем сервер
    config = uvicorn.Config(app=app, host=STT_HOST, port=STT_PORT, log_level=STT_LOG_LEVEL, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())