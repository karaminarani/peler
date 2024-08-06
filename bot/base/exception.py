class ForceStopLoop(Exception):
    """
    Exception raised to forcefully stop a loop, typically used to halt
    the operation of a bot or a service due to an unrecoverable error.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the ForceStopLoop exception with an error message.

        Args:
            message (str): The error message associated with the exception.
        """
        super().__init__(message)
        self.message: str = message
