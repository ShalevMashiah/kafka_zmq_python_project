import json
import threading
import time
from typing import List
import zmq

from globals.enums.response_status import ResponseStatus
from globals.consts.consts import Consts
from globals.consts.const_strings import ConstStrings
from model.data_classes.zmq_request import Request
from infrastructure.interfaces.izmq_server_manager import IZmqServerManager
from model.data_classes.zmq_response import Response
from infrastructure.api.routers.base_router import BaseRouter
from infrastructure.interfaces.iapi_router import IApiRouter
from infrastructure.factories.logger_factory import LoggerFactory
from globals.consts.logger_messages import LoggerMessages
from globals.utils.colors import Colors
from infrastructure.interfaces.ikafka_manager import IKafkaManager


class ZmqServerManager(IZmqServerManager):
    def __init__(self, host: str, port: int, routers: List[IApiRouter], kafka_manager: IKafkaManager):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._address = f"{ConstStrings.BASE_TCP_CONNECTION_STRINGS}{host}:{port}"
        
        self._is_running = False
        self._server_working_thread = None
        self._routers_dict = dict[str, IApiRouter]()
        self._logger = LoggerFactory.get_logger_manager()
        self._include_routers(routers)
        self._kafka_manager = kafka_manager

    def _format_tagged(self, msg: str) -> str:
        return f"{Colors.BOLD}{Colors.CYAN}[ZMQ]{Colors.RESET} {Colors.WHITE}{msg}{Colors.RESET}"
    
    def start(self) -> None:
        self._socket.bind(self._address)
        self._is_running = True
        self._server_working_thread = threading.Thread(
            target=self._server_working_handle, daemon=True)
        self._server_working_thread.start()
        self._logger.log(ConstStrings.LOG_NAME_DEBUG,
                         LoggerMessages.ZMQ_SERVER_BOUND_TO_ADDRESS.format(self._address))
        return self

    def stop(self) -> None:
        self._is_running = False
        if self._server_working_thread:
            self._server_working_thread.join()
        self._socket.close()
        self._context.term()
        self._logger.log(ConstStrings.LOG_NAME_DEBUG,
                         LoggerMessages.ZMQ_SERVER_STOPPED)

    def _server_working_handle(self) -> None:
        while self._is_running:
            try:
                request_str = self._socket.recv_string()
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(
                        LoggerMessages.ZMQ_SERVER_RECEIVED_RAW_REQUEST.format(request_str)
                    ),
                )

                try:
                    request = Request.from_json(request_str)
                    self._logger.log(
                        ConstStrings.LOG_NAME_DEBUG,
                        self._format_tagged(
                            LoggerMessages.ZMQ_SERVER_PARSED_REQUEST.format(
                                request.resource, request.operation, request.data
                            )
                        ),
                    )
                    response = self._handle_request(request)

                except Exception as e:
                    self._logger.log(
                        ConstStrings.LOG_NAME_DEBUG,
                        self._format_tagged(
                            LoggerMessages.ZMQ_SERVER_PARSE_REQUEST_FAILED.format(e)
                        ),
                    )
                    response = Response(
                        status=ResponseStatus.ERROR,
                        data={ConstStrings.ERROR_MESSAGE: f"invalid request: {e}"},
                    )

            except Exception as e:
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(
                        LoggerMessages.ZMQ_SERVER_SOCKET_LOOP_ERROR.format(e)
                    ),
                )
                response = Response(
                    status=ResponseStatus.ERROR,
                    data={ConstStrings.ERROR_MESSAGE: str(e)},
                )

            try:
                resp_str = response.to_json()
                self._socket.send_string(resp_str)
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(
                        LoggerMessages.ZMQ_SERVER_SENT_RESPONSE.format(resp_str)
                    ),
                )
            except Exception as e:
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(LoggerMessages.ZMQ_SERVER_SEND_ERROR.format(e)),
                )
                time.sleep(Consts.ZMQ_SERVER_LOOP_DURATION)

    def _handle_request(self, request: Request) -> Response:
        resource = request.resource
        operation = request.operation
        data = request.data

        if resource == "orders" and operation == "create":
            try:
                payload = dict(data)
                payload["source"] = "ZMQ" 
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(
                        LoggerMessages.ZMQ_SERVER_FORWARDING_TO_KAFKA.format(
                            ConstStrings.ORDER_TOPIC, payload
                        )
                    ),
                )

                self._kafka_manager.send_message(ConstStrings.ORDER_TOPIC, json.dumps(payload))

                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(
                        LoggerMessages.ZMQ_SERVER_FORWARDING_DONE.format(ConstStrings.ORDER_TOPIC)
                    ),
                )

                return Response(
                    status=ResponseStatus.SUCCESS,
                    data={"message": "order sent to kafka", "topic": ConstStrings.ORDER_TOPIC},
                )

            except Exception as e:
                self._logger.log(
                    ConstStrings.LOG_NAME_DEBUG,
                    self._format_tagged(
                        LoggerMessages.ZMQ_SERVER_FORWARDING_FAILED.format(e)
                    ),
                )
                return Response(
                    status=ResponseStatus.ERROR,
                    data={ConstStrings.ERROR_MESSAGE: str(e)},
                )

        if resource in self._routers_dict:
            route = self._routers_dict[resource]
            return route.handle_operation(operation, data)

        return Response(
            status=ResponseStatus.ERROR,
            data={ConstStrings.ERROR_MESSAGE: ConstStrings.UNKNOWN_RESOURCE_ERROR_MESSAGE},
        )

    def _include_routers(self, routers: List[IApiRouter]) -> None:
        for router in routers:
            self._routers_dict[router.resource] = router

        self._logger.log(
            ConstStrings.LOG_NAME_DEBUG,
            self._format_tagged(
                LoggerMessages.ZMQ_SERVER_ROUTERS_REGISTERED.format(list(self._routers_dict.keys()))
            ),
        )