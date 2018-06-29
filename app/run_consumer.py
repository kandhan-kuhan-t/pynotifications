import sys
import importlib
import json


medium = sys.argv[1]
service = sys.argv[2]
broker_url = sys.argv[3]
queue_name = sys.argv[4]
pass_dict = json.loads(sys.argv[5])

i = importlib.import_module(f"app.notifiers.{medium}")
base = importlib.import_module("app.adapters.consumers")
rabbit_consumer_class = getattr(base, "RabbitConsumer")

consumer_class = getattr(i, service)

consumer_instance = consumer_class(
    broker_url=broker_url, queue_name=queue_name, consumer_class=rabbit_consumer_class, **pass_dict
)

consumer_instance.as_consumer().start()





