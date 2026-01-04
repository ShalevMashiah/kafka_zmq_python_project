import os
from infrastructure.factories.infrastructure_factory import InfrastructureFactory
from globals.consts.const_strings import ConstStrings
from infrastructure.interfaces.iexample_manager import IExampleManager
from infrastructure.interfaces.izmq_server_manager import IZmqServerManager
from model.managers.example_manager import ExampleManager
from infrastructure.interfaces.ilogger_manager import ILoggerManager


class ManagerFactory:

    # def _get_config_path() -> str:
    #     factories_dir = os.path.dirname(os.path.abspath(__file__))
    #     infra_root = os.path.dirname(factories_dir)
    #     config_path = os.path.join(infra_root, "config", "configuration.xml")
    #     return config_path
    _kafka_manager = None
    _zmq_server_manager = None

    @staticmethod
    def create_example_manager() -> IExampleManager:
        config_manager = InfrastructureFactory.create_config_manager(
            ConstStrings.GLOBAL_CONFIG_PATH)
        ManagerFactory._kafka_manager = InfrastructureFactory.create_kafka_manager(config_manager)

        return ExampleManager(config_manager, ManagerFactory._kafka_manager)

    @staticmethod
    def create_example_zmq_manager() -> IZmqServerManager:
        if ManagerFactory._kafka_manager is None:
            ManagerFactory.create_example_manager()

        zmq_server_manager = InfrastructureFactory.create_zmq_server_manager(ManagerFactory._kafka_manager)
        ManagerFactory._zmq_server_manager = zmq_server_manager
        return zmq_server_manager

    @staticmethod
    def create_all():
        # Consumer only needs to consume from Kafka - no ZMQ server needed
        ManagerFactory.create_example_manager()
        # ManagerFactory.create_example_zmq_manager()
