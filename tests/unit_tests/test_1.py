import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.auth import AuthService



def test_create_and_decode_access_token():
    data = {"user_id": 1}
    result = AuthService.create_access_token(data)
    assert result
    assert isinstance(result, str)

    payload = AuthService.decode_token(result)

    assert payload
    assert payload["user_id"] == data["user_id"]