class LoggerMessages:
    DEFAULT_ERROR = 'ERROR'
    ZMQ_SERVER_BOUND_TO_ADDRESS = "ZMQ REP server bound to {}"
    ZMQ_SERVER_STOPPED = "ZMQ REP server stopped"
    EXAMPLE_DATA_RECEIVED = "example data received: {}"
    CONFIG_KEY_NOT_FOUND = "xmlconfig: key '{}' not found."
    CONFIG_DID_YOU_MEAN = "xmlconfig: did you mean '{}'?"
    CONFIG_NO_MATCHES = "xmlconfig: no close matches found."
    KAFKA_TOPIC_ALREADY_CONSUMING = "Already consuming topic: {}"
    KAFKA_TOPIC_NOT_EXIST = "Topic Not Exist"
    EXAMPLE_PRINT_CONSUMER_MSG = ", message is: {}"
    KAFKA_TOPIC = "Kafka topic: {}"

    # ---------------- Orders UI ----------------
    ORDER_PRINT_CONSUMER_MSG = "Order event #{} received"
    ORDER_EVENT = "[ORDER EVENT]"
    ORDER_TOPIC = "Topic:"
    ORDER_MESSAGE = "Message:"

        # ---------------- ZMQ SERVER ----------------
    ZMQ_SERVER_BOUND_TO_ADDRESS = "ZMQ REP server bound to {}"
    ZMQ_SERVER_STOPPED = "ZMQ REP server stopped"
    ZMQ_SERVER_RECEIVED_RAW_REQUEST = "ZMQ server received raw request: {}"
    ZMQ_SERVER_PARSED_REQUEST = "ZMQ server parsed request. resource='{}', operation='{}', data={}"
    ZMQ_SERVER_PARSE_REQUEST_FAILED = "ZMQ server failed to parse request: {}"
    ZMQ_SERVER_SOCKET_LOOP_ERROR = "ZMQ server loop error: {}"
    ZMQ_SERVER_SENT_RESPONSE = "ZMQ server sent response: {}"
    ZMQ_SERVER_SEND_ERROR = "ZMQ server failed sending response: {}"
    ZMQ_SERVER_FORWARDING_TO_KAFKA = "ZMQ → Kafka: forwarding to topic '{}' with payload: {}"
    ZMQ_SERVER_FORWARDING_DONE = "ZMQ → Kafka: message forwarded successfully to topic '{}'"
    ZMQ_SERVER_FORWARDING_FAILED = "ZMQ → Kafka: forwarding failed: {}"
    ZMQ_SERVER_ROUTERS_REGISTERED = "ZMQ server routers registered: {}"

        # ---------------- ZMQ CLIENT ----------------
    ZMQ_CLIENT_CONNECTED = "ZMQ client connected to {}"
    ZMQ_CLIENT_DISCONNECTED = "ZMQ client disconnected from {}"
    ZMQ_CLIENT_SENDING_REQUEST = "ZMQ client sending request: {}"
    ZMQ_CLIENT_RECEIVED_RESPONSE = "ZMQ client received response: {}"
    ZMQ_CLIENT_ERROR = "ZMQ client error: {}"