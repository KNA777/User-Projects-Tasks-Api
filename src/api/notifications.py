from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import asyncio

from src.services.auth import AuthService
from src.services.sse_manager import sse_manager
from src.api.dependencies import DBDep

from fastapi.responses import HTMLResponse

from src.services.users import UserService

router = APIRouter(prefix="/notifications", tags=["SSE Notifications"])


@router.get("/stream")
async def sse_stream(
        db: DBDep,
        token: str = Query(None)

):

    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    try:
        # Декодируем токен
        payload = AuthService.decode_token(token)
        user_id = payload["user_id"]

        # Проверяем что пользователь существует
        user = await UserService(db).get_user(id=user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        print(f"✅ SSE подключение для user_id: {user_id}")

        async def event_generator():
            queue = asyncio.Queue()
            await sse_manager.add_connection(user_id, queue)

            try:
                while True:
                    event_data = await queue.get()
                    yield f"data: {event_data}\n\n"
            except asyncio.CancelledError:
                await sse_manager.remove_connection(user_id, queue)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        print(f"❌ Ошибка аутентификации: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/get-token")
async def get_test_token(db: DBDep):
    """Получить тестовый токен (для разработки)"""
    # Находим тестового пользователя
    user = await UserService(db).get_user(email="user@example.com")
    if not user:
        raise HTTPException(status_code=404, detail="Test user not found")

    # Создаем токен
    token = AuthService.create_access_token({"user_id": user.id})

    return {"token": token, "user_id": user.id, "email": user.email}


@router.get("/test-page", response_class=HTMLResponse)
async def sse_test_page():
    """Тестовая страница для SSE"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SSE Тест</title>
        <style>
            .notification { 
                border: 1px solid #ccc; 
                padding: 15px; 
                margin: 10px; 
                border-radius: 8px;
                font-family: Arial, sans-serif;
            }
            .task { 
                background: #e3f2fd; 
                border-left: 4px solid #2196f3;
            }
            .comment { 
                background: #f3e5f5; 
                border-left: 4px solid #9c27b0;
            }
            .success { background: #e8f5e8; border-left: 4px solid #4caf50; }
            .error { background: #ffebee; border-left: 4px solid #f44336; }
            .info { background: #e3f2fd; border-left: 4px solid #2196f3; }

            .notification strong { color: #333; }
            .notification small { color: #666; font-size: 12px; }
            .comment-content { 
                background: white; 
                padding: 10px; 
                margin: 8px 0; 
                border-radius: 4px; 
                border: 1px solid #ddd;
            }

            #tokenInput {
                width: 400px; 
                padding: 8px; 
                margin-right: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            button {
                padding: 8px 16px;
                background: #4caf50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }

            button:hover {
                background: #45a049;
            }

            #notifications {
                margin-top: 20px;
                max-height: 600px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <h1>SSE Уведомления - Тестовая страница</h1>
        <div>
            <input type="text" id="tokenInput" placeholder="Введите JWT token">
            <button onclick="connectSSE()">Подключиться</button>
            <button onclick="disconnectSSE()" style="background: #f44336;">Отключиться</button>
        </div>
        <div id="notifications"></div>

        <script>
            let eventSource = null;

            function connectSSE() {
                const token = document.getElementById('tokenInput').value;
                if (!token) {
                    alert('Введите JWT token');
                    return;
                }

                // Закрываем предыдущее соединение
                if (eventSource) {
                    eventSource.close();
                }

                const url = new URL('/notifications/stream', window.location.origin);
                url.searchParams.append('token', token);
                console.log('Подключаемся к:', url.toString());

                eventSource = new EventSource(url.toString());

                eventSource.onmessage = function(event) {
                    try {
                        const notification = JSON.parse(event.data);
                        console.log('📨 Получено уведомление:', notification);
                        showNotification(notification);
                    } catch (error) {
                        console.error('Ошибка парсинга уведомления:', error, event.data);
                    }
                };

                eventSource.onerror = function(error) {
                    console.error('SSE Ошибка:', error);
                    addNotification('❌ Ошибка подключения к SSE серверу', 'error');
                };

                eventSource.onopen = function() {
                    console.log('SSE соединение установлено');
                    addNotification('✅ Подключено к SSE серверу', 'success');
                };

                addNotification('🔄 Подключаемся к SSE...', 'info');
            }

            function disconnectSSE() {
                if (eventSource) {
                    eventSource.close();
                    eventSource = null;
                    addNotification('🔌 Отключено от SSE сервера', 'info');
                }
            }

            function showNotification(notification) {
                let typeClass = 'info';
                let title = 'Уведомление';
                let content = '';

                // Определяем тип уведомления и формируем содержимое
                if (notification.comment_content) {
                    typeClass = 'comment';
                    title = '💬 Новый комментарий';
                    content = `
                        <p><strong>Задача:</strong> ${notification.task_title || 'Неизвестная задача'}</p>
                        <p><strong>Автор:</strong> ${notification.author_name || 'Неизвестный автор'}</p>
                        <div class="comment-content">
                            <strong>Текст комментария:</strong><br>
                            ${notification.comment_content || 'Нет текста'}
                        </div>
                    `;
                } else if (notification.task_title) {
                    typeClass = 'task';
                    title = '🎯 Новая задача';
                    content = `
                        <p><strong>Задача:</strong> ${notification.task_title || 'Неизвестная задача'}</p>
                        <p><strong>Проект:</strong> ${notification.project_name || 'Неизвестный проект'}</p>
                        <p>${notification.message}</p>
                    `;
                } else {
                    // Общее уведомление
                    content = `<p>${notification.message || 'Нет сообщения'}</p>`;
                }

                const div = document.createElement('div');
                div.className = `notification ${typeClass}`;
                div.innerHTML = `
                    <strong>${title}</strong><br>
                    ${content}
                    <small>${new Date(notification.timestamp || new Date()).toLocaleString()}</small>
                `;

                const container = document.getElementById('notifications');
                container.prepend(div);

                // Браузерное уведомление
                if ('Notification' in window && Notification.permission === 'granted') {
                    new Notification(title, {
                        body: notification.message || notification.comment_content || 'Новое уведомление'
                    });
                }
            }

            function addNotification(message, type = 'info') {
                const div = document.createElement('div');
                div.className = `notification ${type}`;
                div.innerHTML = message;
                document.getElementById('notifications').prepend(div);
            }

            // Запрос разрешения на уведомления
            if ('Notification' in window && Notification.permission === 'default') {
                Notification.requestPermission().then(function(permission) {
                    if (permission === 'granted') {
                        console.log('Разрешение на уведомления получено');
                    }
                });
            }

            // Автозаполнение токена из localStorage
            const savedToken = localStorage.getItem('sse_token');
            if (savedToken) {
                document.getElementById('tokenInput').value = savedToken;
            }

            // Сохранение токена при изменении
            document.getElementById('tokenInput').addEventListener('change', function() {
                localStorage.setItem('sse_token', this.value);
            });

            // Автоподключение при загрузке если есть токен
            window.addEventListener('load', function() {
                const savedToken = localStorage.getItem('sse_token');
                if (savedToken) {
                    setTimeout(connectSSE, 1000); // Небольшая задержка для загрузки страницы
                }
            });
        </script>
    </body>
    </html>
    """