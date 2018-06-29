from app import orchestrator

runner = orchestrator.run()

producer = orchestrator.get_producer('email')

producer.send(
    from_name="kandhan",
    from_address="test_notipy@mail.cyces.co",
    to_name="kandhan",
    to_address="kandhan@cyces.co",
    subject="waiter!!",
    message_html="<h2>Yay!</h2>",
    message_text="Yay!",
    callback_data={"id": 0}
)


import time


while True:
    time.sleep(1)