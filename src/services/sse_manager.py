import asyncio
from typing import Dict, Set
import json


class SSEManager:
    """
    Менеджер для управления подключениями SSE.
    Хранит очереди сообщений для каждого пользователя.
    """

    def __init__(self):
        # user_id -> set of queues для этого пользователя
        self.connections: Dict[int, Set[asyncio.Queue]] = {}

    async def add_connection(self, user_id: int, queue: asyncio.Queue):
        """Добавляет новое подключение для пользователя"""
        if user_id not in self.connections:
            self.connections[user_id] = set()
        self.connections[user_id].add(queue)
        print(f"✅ Добавлено SSE подключение для user_id: {user_id}")

    async def remove_connection(self, user_id: int, queue: asyncio.Queue):
        """Удаляет подключение пользователя"""
        if user_id in self.connections:
            self.connections[user_id].discard(queue)
            if not self.connections[user_id]:
                del self.connections[user_id]
            print(f"❌ Удалено SSE подключение для user_id: {user_id}")

    async def send_event(self, user_id: int, event: dict):
        """Отправляет событие конкретному пользователю"""
        if user_id in self.connections:
            event_json = json.dumps(event)
            for queue in self.connections[user_id]:
                await queue.put(event_json)
            print(f"📨 Отправлено событие user_id {user_id}: {event['type']}")


# Глобальный экземпляр менеджера
sse_manager = SSEManager()