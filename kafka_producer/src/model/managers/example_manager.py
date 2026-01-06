import os
import time
import threading
import json

from infrastructure.interfaces.iexample_manager import IExampleManager
from infrastructure.interfaces.iconfig_manager import IConfigManager
from infrastructure.interfaces.ikafka_manager import IKafkaManager
from globals.consts.const_strings import ConstStrings
from globals.consts.consts import Consts
from globals.consts.logger_messages import LoggerMessages
from infrastructure.factories.logger_factory import LoggerFactory
from globals.utils.colors import Colors
from infrastructure.events.zmq_client_manager import ZmqClientManager
from model.data_classes.zmq_request import Request

class ExampleManager(IExampleManager):
    def __init__(self, config_manager: IConfigManager, kafka_manager: IKafkaManager) -> None:
        super().__init__()
        self.order_id_counter = 0
        self._config_manager = config_manager
        self._kafka_manager = kafka_manager
        self._example_topic_consumer = ConstStrings.EXAMPLE_TOPIC
        self._logger = LoggerFactory.get_logger_manager()
        self._await_lock = threading.Lock()
        self._awaited_order_id = None
        self._await_event = threading.Event()
        host = os.getenv(ConstStrings.ZMQ_SERVER_HOST) 
        port = int(os.getenv(ConstStrings.ZMQ_SERVER_PORT))
        self._zmq_client = ZmqClientManager(host, port)
        self._zmq_client.start()

        self._init_threading()

    def do_something(self) -> None:
        pass

    def _init_threading(self) -> None:
        self._message_produce_threading = threading.Thread(
            target=self._produce_kafka_message
        )
        self._message_produce_threading.start()

    def _produce_kafka_message(self) -> None:
        while True:
            time.sleep(Consts.SEND_MESSAGE_DURATION)

            current_id = self.order_id_counter
           

            order = {
                "order_id": current_id,
                "customer": f"Customer {current_id}",
                "items": ["Pizza", "Drink"],
                "total_price": 89.90,
                "status": "CREATED",
            }

            with self._await_lock:
                self._awaited_order_id = current_id
                self._await_event.clear()

            req = Request(resource="orders", operation="create", data=order)
            resp = self._zmq_client.send_request(req)
            
            got_it = self._await_event.wait(timeout=10)

            if not got_it:
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    f"[PRODUCER] Timeout waiting for Kafka consume of order_id={current_id}"
                )
            self.order_id_counter += 1