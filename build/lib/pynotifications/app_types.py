from typing import Callable
from abc import ABC


class ConsumerImplementation(ABC):

    def __init__(self, url: str, queue_name: str, process_task_function: Callable, call_on_success: bool,
                 call_on_failure: bool) -> None: ...

