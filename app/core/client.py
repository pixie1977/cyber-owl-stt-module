"""
Клиент для взаимодействия с STT-сервером.
Отправляет запросы на распознавание и получает результаты.
"""

import asyncio
import aiohttp
from typing import Optional


class PostClient:
    """
    Асинхронный post-клиент для работы с API.
    """

    def __init__(self, url: str):
        """
        Инициализация клиента.

        :param url: URL сервера.
        """
        self.url = url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "PostClient":
        """
        Контекстный менеджер: открывает сессию.
        """
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Контекстный менеджер: закрывает сессию.
        """
        if self.session:
            await self.session.close()

    async def post(self, text: str) -> bool:
        """
        Отправляет текстовую строку на сервер через POST-запрос.

        :param text: текст для отправки.
        :return: True, если запрос успешен.
        """
        if not self.session:
            print("❌ Сессия не открыта. Используйте контекстный менеджер.")
            return False

        try:
            async with self.session.post(
                f"{self.url}",
                json={"text": text}
            ) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"❌ Ошибка при отправке текста: {e}")
            return False

    async def get_latest_transcript(self) -> str:
        """
        Получает последнюю распознанную фразу с сервера.

        :return: Текст транскрипции или пустая строка.
        """
        if not self.session:
            print("❌ Сессия не открыта. Используйте контекстный менеджер.")
            return ""

        try:
            async with self.session.get(f"{self.url}/latest") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("transcript", "").strip()
                return ""
        except Exception as e:
            print(f"❌ Ошибка при получении транскрипции: {e}")
            return ""

    async def poll_transcripts(self, interval: float = 2.0):
        """
        Периодически опрашивает сервер и возвращает новые распознанные фразы.

        :param interval: интервал опроса в секундах.
        :yields: распознанный текст (не пустой).
        """
        last_text = ""
        while True:
            transcript = await self.get_latest_transcript()
            if transcript and transcript != last_text:
                last_text = transcript
                yield transcript
            await asyncio.sleep(interval)


# Пример использования
async def main():
    """
    Пример асинхронного использования клиента.
    """
    async with PostClient("http://127.0.0.1:8082/api/tts/json") as client:
        # Пример отправки текста
        success = await client.post("Это тестовое сообщение от клиента.")
        if success:
            print("✅ Сообщение отправлено")
        else:
            print("❌ Не удалось отправить сообщение")

        print("📝 Начинаем опрос сервера каждые 1.5 секунды...")
        async for text in client.poll_transcripts(interval=1.5):
            print(f"💬 Получено: {text}")


if __name__ == "__main__":
    asyncio.run(main())