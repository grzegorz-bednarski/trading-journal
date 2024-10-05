class CoreError(Exception):
    error_message = None

    def __init__(self, message: str | None = None):
        self.message = message or self.error_message
        super().__init__(self.message)
