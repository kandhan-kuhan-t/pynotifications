import requests
from typing import Dict
import app.exceptions


def post(data: Dict,  url: str, headers: Dict = None, json: bool = True):
    headers = headers if headers is not None else {}
    try:
        if json:
            r = requests.post(
                url=url,
                json=data,
                headers=headers
            )
        else:
            r = requests.post(
                url=url,
                data=data,
                headers=headers
            )
        if r.status_code not in (200, 201):
            raise app.exceptions.ResponseNot200(r.text)
        return r.text
    except requests.ConnectionError as e:
        raise app.exceptions.NoConnection(f"{url} cannot be called")


def get_producer_for_failed_tasks(url: str, original_queue_name: str, connector_class):
    ...