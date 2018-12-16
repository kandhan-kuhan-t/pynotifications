import os
import json
import subprocess
import pynotifications.adapters.producers
import pynotifications.adapters.connectors


cur_dir = os.path.dirname(os.path.realpath(__file__))
_producers = {}


def read_data_from_conf_file(file_path=f"{cur_dir}/../notipy.conf.json"):
    with open(file_path, "r") as f:
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
            "consumer_python": data["consumer_python"],
            "call_on_success": data["call_on_success"],
            "call_on_failure": data["call_on_failure"],
            "log_directory": data["log_directory"]
        }


def get_producer(name: str):
    return _producers[name]


def run_consumer(conf):
    command = f"{conf['consumer_python']} {cur_dir}/run_consumer.py " \
              f"{conf['medium']} {conf['service']} {conf['broker_url']} {conf['name']}"
    if conf.get('medium') == 'dynamic':
        last_arg = json.dumps(
            dict(
                call_on_success=conf.get('call_on_success'),
                call_on_failure=conf.get('call_on_failure')
            )
        )
    else:
        last_arg = json.dumps(
            dict(
                http_call_url=conf.get('http_call_url'),
                http_headers=conf.get('http_headers'),
                call_on_success=conf.get('call_on_success'),
                call_on_failure=conf.get('call_on_failure')
            )
        )
    p = subprocess.Popen(
        [*command.split(' '), last_arg, '&']
        # stdout=open(cur_dir+'/sys.out', 'w'),
        # stderr=open(cur_dir+'/sys.out', 'w'),
    )
    return p


def create_producer(conf):
    if conf["medium"] == "email":
        producer = pynotifications.adapters.producers.Email(
            url=conf["broker_url"],
            queue_name=conf["name"],
            connector_cls=pynotifications.adapters.connectors.RabbitConnector,
            callback_url=conf["callback_url"],
        )
    elif conf["medium"] == "dynamic":
        producer = pynotifications.adapters.producers.DynamicProducer(
            url=conf["broker_url"],
            queue_name=conf["name"],
            connector_cls=pynotifications.adapters.connectors.RabbitConnector,
            callback_url=conf["callback_url"],
        )
    else:
        raise Exception(f"no producer configured for {conf['medium']}")
    if producer is not None:
        _producers[conf["name"]] = producer


def run(conf, should_create_consumer: bool = True):
    if should_create_consumer:
        consumer = run_consumer(conf)

    create_producer(conf)

    import atexit, time

    @atexit.register
    def goodbye():
        if should_create_consumer:
            i = 3
            while i:
                print('waiting for consumer to terminate..')
                time.sleep(1)
                i -= 1
            consumer.terminate()

    class c:
        @staticmethod
        def stop():
            if should_create_consumer:
                consumer.terminate()

    return c

