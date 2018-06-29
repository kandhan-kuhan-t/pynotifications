from typing import TypeVar, Generic, Callable, Dict, NewType, Any
from abc import ABC, abstractmethod


class ConsumerImplementation(ABC):

    def __init__(self, url: str, queue_name: str, process_task_function: Callable) -> None: ...


# CONSUMER_IMPLEMENTATION = NewType('CONSUMER_IMPLEMENTATION', Any)

