import sys
import importlib
import json


medium = sys.argv[1]
service = sys.argv[2]
broker_url = sys.argv[3]
queue_name = sys.argv[4]
pass_dict = json.loads(sys.argv[5])

if medium == 'dynamic':
    i = importlib.import_module(f"pynotifications.adapters.mediums.dynamic")
    consumer_class = getattr(i, "Medium")

else:
    i = importlib.import_module(f"pynotifications.notifiers.{medium}")
    consumer_class = getattr(i, service)

base = importlib.import_module("pynotifications.adapters.consumers.rabbit")
rabbit_consumer_class = getattr(base, "RabbitConsumer")

consumer_instance = consumer_class(
    broker_url=broker_url, queue_name=queue_name, consumer_class=rabbit_consumer_class, **pass_dict
)

consumer_instance.as_consumer().start()
