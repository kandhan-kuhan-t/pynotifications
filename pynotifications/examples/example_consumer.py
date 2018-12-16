from pynotifications.adapters.connectors import RabbitConnector
from pynotifications.adapters.consumers import RabbitConsumer
from pynotifications.adapters.producers import Email
from pynotifications.notifiers.email import SparkPost

queue_name = "damn"

producer = Email(
    url="amqp://kilobyte:lolcats123@localhost:5672/test",
    queue_name=queue_name,
    connector_cls=RabbitConnector,
    callback_url="http://localhost/notipy/callback"
)
producer.send(
    from_name="kandhan",
    from_address="test_notipy@mail.cyces.co",
    to_name="kandhan",
    to_address="kandhan@cyces.co",
    subject="test",
    message_html="<h2>Yay!</h2>",
    message_text="Yay!",
    callback_data={"id": 0}
)

rabbit = SparkPost(
    broker_url="amqp://kilobyte:lolcats123@localhost:5672/test",
    queue_name=queue_name,
    consumer_class=RabbitConsumer,
    http_headers={"Authorization": "ec77d525193a9dfd5fabfc69a65183af58f5a20d"},
    http_call_url="https://api.sparkpost.com/api/v1/transmissions"
).as_consumer()

rabbit.start()
