import os
from infrastructure.factories.infrastructure_factory import InfrastructureFactory
from globals.consts.const_strings import ConstStrings
from infrastructure.interfaces.iexample_manager import IExampleManager
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
    def create_all():
        ManagerFactory.create_example_manager()
