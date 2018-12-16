from adapters.connectors import RabbitConnector
from adapters.consumers import RabbitConsumer
from notifiers.sms import Twilio

producer = RabbitConnector(url="amqp://kilobyte:lolcats123@localhost:5672/test", queue_name="twilio_sms")
producer.push_to_queue(
    {
        "context": {
            "from": {
                "number": "+18043755316"
            },
            "to": {
                "number": "+918903121126"
            },
            "message": "test from notipy"
        },
        "success_callback_url": "http://localhost/sukkess",
        "failure_callback_url": "http://localhost/failure",
        "callback_data": {}
    }
)

rabbit = Twilio(
    broker_url="amqp://kilobyte:lolcats123@localhost:5672/test",
    queue_name="twilio_sms",
    consumer_class=RabbitConsumer,
).as_consumer()

rabbit.start()
