from fastapi.openapi.models import Example

OPENAPI_EXAMPLES_REG = openapi_examples = {
            "Example 1": Example(
                summary="Пример №1",
                value={
                    "username": "user1",
                    "email": "user@example.com",
                    "password": "string",
                    "superuser_psw": "string"
                }
            ),
            "Example 2": Example(
                summary="Пример №2",
                value={
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "string",
                    "superuser_psw": "string"
                }
            ),
            "Example 3": Example(
                summary="Пример №3",
                value={
                    "username": "user3",
                    "email": "user3@example.com",
                    "password": "string",
                    "superuser_psw": "string"
                }
            )
}

OPENAPI_EXAMPLES_LOGIN = openapi_examples = {
            "Example 1": Example(
                summary="Пример №1",
                value={
                    "email": "user@example.com",
                    "password": "string",
                }
            ),
            "Example 2": Example(
                summary="Пример №2",
                value={
                    "email": "user2@example.com",
                    "password": "string",
                }
            ),
            "Example 3": Example(
                summary="Пример №3",
                value={
                    "email": "user3@example.com",
                    "password": "string",
                }
            )
}