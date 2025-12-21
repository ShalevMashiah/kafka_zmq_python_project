
import zmq

from globals.enums.response_status import ResponseStatus
from globals.consts.const_strings import ConstStrings
from infrastructure.interfaces.izmq_client_manager import IZmqClientManager
from model.data_classes.zmq_request import Request
from model.data_classes.zmq_response import Response
from globals.consts.logger_messages import LoggerMessages
from infrastructure.factories.logger_factory import LoggerFactory
from globals.utils.colors import Colors


class ZmqClientManager(IZmqClientManager):
    def __init__(self, host: str, port: int):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._address = f"{ConstStrings.BASE_TCP_CONNECTION_STRINGS}{host}:{port}"
        self._logger = LoggerFactory.get_logger_manager()
        
    def _tag(self, msg: str) -> str:
        return f"{Colors.BOLD}{Colors.MAGENTA}[ZMQ-CLIENT]{Colors.RESET} {msg}"

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
            req_str = request.to_json()

            self._logger.log(
                ConstStrings.LOG_NAME_DEBUG,
                self._tag(LoggerMessages.ZMQ_CLIENT_SENDING_REQUEST.format(req_str)),
            )

            self._socket.send_string(req_str)
            resp_str = self._socket.recv_string()

            self._logger.log(
                ConstStrings.LOG_NAME_DEBUG,
                self._tag(LoggerMessages.ZMQ_CLIENT_RECEIVED_RESPONSE.format(resp_str)),
            )

            return Response.from_json(resp_str)

        except Exception as e:
            self._logger.log(
                ConstStrings.LOG_NAME_DEBUG,
                self._tag(LoggerMessages.ZMQ_CLIENT_ERROR.format(str(e))),
            )
            return Response(
                status=ResponseStatus.ERROR,
                data={ConstStrings.ERROR_MESSAGE: str(e)},
            )
