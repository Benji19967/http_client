class ClientError(Exception):
    """
    Raised when a client sends an invalid request
    """

    pass


class ServerError(Exception):
    """
    Raised when a server encountered an error when handling a request
    """

    pass
