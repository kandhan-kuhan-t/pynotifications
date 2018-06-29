import os
import json
import subprocess
import app.adapters.producers
import app.adapters.connectors


cur_dir = os.path.dirname(os.path.realpath(__file__))
_producers = {}


def read_data_from_conf_file():
    with open(f"{cur_dir}/../notipy.conf.json", "r") as f:
        data = json.load(f)
        return {
            "broker_url": data["broker_url"],
            "connector_class": data["connector_class"],
            "callback_url": data["callback_url"],
            "name": data["name"],
            "medium": data["medium"],
            "service": data["service"],
            "http_call_url": data["http_call_url"],
            "http_headers": data["http_headers"],
            "consumer_python": data["consumer_python"]
        }


def get_producer(name: str):
    return _producers[name]


def run_consumer(conf):
    command = f"{conf['consumer_python']} {cur_dir}/run_consumer.py " \
              f"{conf['medium']} {conf['service']} {conf['broker_url']} {conf['name']}"
    last_arg = json.dumps(
        dict(http_call_url=conf.get('http_call_url'), http_headers=conf.get('http_headers'))
    )
    p = subprocess.Popen(
        [*command.split(' '), last_arg, '&'],
        stdout=open(cur_dir+'/sys.out', 'w'),
        stderr=open(cur_dir+'/sys.out', 'w'),
    )
    return p


def create_producer(conf):
    producer = app.adapters.producers.Email(
        url=conf["broker_url"],
        queue_name=conf["name"],
        connector_cls=app.adapters.connectors.RabbitConnector,
        callback_url="http://localhost:8000/callback"
    )
    _producers[conf["name"]] = producer


def run():
    conf = read_data_from_conf_file()
    consumer = run_consumer(conf)
    create_producer(conf)

    import atexit, time

    @atexit.register
    def goodbye():
        i = 3
        while i:
            print('waiting for consumer to terminate..')
            time.sleep(1)
            i -= 1
        consumer.terminate()

    class c:
        @staticmethod
        def stop():
            consumer.terminate()

    return c
