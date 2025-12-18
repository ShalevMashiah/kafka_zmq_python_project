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


class ExampleManager(IExampleManager):
    def __init__(self, config_manager: IConfigManager, kafka_manager: IKafkaManager) -> None:
        super().__init__()
        self.order_id_counter = 1
        self._config_manager = config_manager
        self._kafka_manager = kafka_manager
        self._example_topic_consumer = ConstStrings.EXAMPLE_TOPIC
        self._logger = LoggerFactory.get_logger_manager()
        self._init_threading()
        self._init_consumers()

    def do_something(self) -> None:
        pass

    def _init_threading(self) -> None:
        self._message_produce_threading = threading.Thread(
            target=self._produce_kafka_message
        )
        self._message_produce_threading.start()

    def _init_consumers(self) -> None:
        self._kafka_manager.start_consuming(
            self._example_topic_consumer, self._print_consumer)

    def _produce_kafka_message(self) -> None:
        while (True):
            time.sleep(Consts.SEND_MESSAGE_DURATION)
            order = {
                "order_id": self.order_id_counter,
                "customer": f"Customer {self.order_id_counter}",
                "items": ["Pizza", "Drink"],
                "total_price": 89.90,
                "status": "CREATED",
            }
            message = json.dumps(order)
            
            self._kafka_manager.send_message(
                ConstStrings.EXAMPLE_TOPIC, message)

    def _print_consumer(self, msg: str) -> None:
        # self._logger.log(ConstStrings.LOG_NAME_DEBUG,
        #                  LoggerMessages.EXAMPLE_PRINT_CONSUMER_MSG.format(str(msg)))
        try:
            data = json.loads(msg)
        except Exception:
            print("Failed to parse message as JSON.")
            data = msg

        formatted = (
            f"{Colors.RESET}{Colors.BOLD}{Colors.BLUE}"
            f"{LoggerMessages.ORDER_PRINT_CONSUMER_MSG.format(self.order_id_counter)}"
            f"{Colors.RESET}\n"
            f"{Colors.CYAN}{LoggerMessages.ORDER_EVENT} "
            f"{Colors.BOLD}{Colors.YELLOW}{LoggerMessages.ORDER_TOPIC}{Colors.RESET} "
            f"{Colors.GREEN}{self._example_topic_consumer}{Colors.RESET}\n"
            f"{Colors.BOLD}{Colors.MAGENTA}{LoggerMessages.ORDER_MESSAGE}{Colors.RESET} "
            f"{Colors.WHITE}{json.dumps(data, indent=4)}{Colors.RESET}"
        )
        
        self._logger.log(ConstStrings.LOG_NAME_DEBUG, formatted)
        self.order_id_counter += 1
