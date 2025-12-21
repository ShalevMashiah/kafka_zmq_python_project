
import zmq

from globals.enums.response_status import ResponseStatus
from globals.consts.const_strings import ConstStrings
from infrastructure.interfaces.izmq_client_manager import IZmqClientManager
from model.data_classes.zmq_request import Request
from model.data_classes.zmq_response import Response
from globals.consts.logger_messages import LoggerMessages
from infrastructure.factories.logger_factory import LoggerFactory


class ZmqClientManager(IZmqClientManager):
    def __init__(self, host: str, port: int):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._address = f"{ConstStrings.BASE_TCP_CONNECTION_STRINGS}{host}:{port}"
        self._logger = LoggerFactory.get_logger_manager()


    def start(self) -> None:
        self._socket.connect(self._address)
        self._logger.log(
            ConstStrings.LOG_NAME_DEBUG,
            self._tag(LoggerMessages.ZMQ_CLIENT_CONNECTED.format(self._address)),
        )

    def stop(self) -> None:
        self._socket.close()
        self._logger.log(
            ConstStrings.LOG_NAME_DEBUG,
            self._tag(LoggerMessages.ZMQ_CLIENT_DISCONNECTED.format(self._address)),
        )
    
    def send_request(self, request: Request) -> Response:
        try:
            self._logger.log(
                ConstStrings.LOG_NAME_DEBUG,
                self._tag(
                    LoggerMessages.ZMQ_CLIENT_SENDING_REQUEST.format(
                        request.to_json()
                    )
                ),
            )

            self._socket.send_json(request.to_json())
            resp_dict = self._socket.recv_json()

            self._logger.log(
                ConstStrings.LOG_NAME_DEBUG,
                self._tag(
                    LoggerMessages.ZMQ_CLIENT_RECEIVED_RESPONSE.format(resp_dict)
                ),
            )

            return Response.from_json(resp_dict)
        except Exception as e:
            self._logger.log(
                ConstStrings.LOG_NAME_DEBUG,
                self._tag(LoggerMessages.ZMQ_CLIENT_ERROR.format(str(e))),
            )
            return Response(
                status=ResponseStatus.ERROR,
                data={ConstStrings.ERROR_MESSAGE: str(e)},
            )