"""Telegram abstractions"""
from json import loads
from typing import Optional, Union
from requests import JSONDecodeError
from requests_toolbelt import sessions

from requests.models import Response
from requests.exceptions import HTTPError, ConnectionError, Timeout


class Telegram:
    """Lightweight Telegram send* abstraction"""

    api = sessions.BaseUrlSession(base_url="https://api.telegram.org")

    def __init__(self, token: str) -> None:
        self.uid = f"/bot{token}"

    def dispatch_call(
        self, method: str, params: dict, data: Optional[dict] = None
    ) -> Optional[dict]:
        """Dispatch prepared call with GET method"""
        try:
            resource: str = f"{self.uid}/{method}"
            response: Response = self.api.get(resource, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            self.http_error(http_err)
        except (Timeout, ConnectionError) as conn_err:
            self.conn_error(conn_err)
        return None

    def send_messsage(
        self,
        chat_id: str,
        message: str,
        reply_markup: Optional[dict] = None,
        method: str = "sendMessage",
        **kwargs,
    ) -> Optional[dict]:
        """Prepare and send message to destination"""
        data: dict = {}
        if reply_markup:
            data.update({"reply_markup": reply_markup})
        params: dict = {"chat_id": chat_id, "text": message, **kwargs}
        return self.dispatch_call(method, params, data)

    def send_sticker(
        self, chat_id: str, sticker: str, method: str = "sendSticker"
    ) -> dict:
        """Prepare and send sticker to destination"""
        return self.dispatch_call(method, {"chat_id": chat_id, "sticker": sticker})

    @staticmethod
    def http_error(http_error: HTTPError, message: str = "") -> None:
        """Log http error to console"""
        response_text = http_error.response.text
        try:
            message = loads(response_text).get("description")
        except JSONDecodeError as json_error:
            message = f"Unknown Error {response_text}"
            print(json_error)

        print(
            type(http_error).__name__,
            http_error.request.path_url,
            "=>",
            http_error.response.status_code,
            message,
        )

    @staticmethod
    def conn_error(conn_error: Union[Timeout, ConnectionError]) -> None:
        """Log a connection error to console"""
        print(type(conn_error).__name__, conn_error.request.url)
