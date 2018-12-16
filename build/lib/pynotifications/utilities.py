import requests
from typing import Dict
import pynotifications.exceptions
import logging.handlers

default_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
fh = logging.handlers.RotatingFileHandler('/var/log/pyNotifications/requests.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(default_formatter)

logger = logging.getLogger("pynotifications_requests")
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


def post(data: Dict,  url: str, headers: Dict = None, json: bool = True):
    headers = headers if headers is not None else {}
    logger.info(f"url: {url}, json: {json}")
    logger.info(f"data: {data}, headers: {headers}")
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
            raise pynotifications.exceptions.ResponseNot200(r.text, status_code=str(r.status_code))
        logger.info(f"status: {r.status_code}, response: {r.text}")
        return r.text
    except requests.ConnectionError as e:
        raise pynotifications.exceptions.NoConnection(f"{url} cannot be called")
