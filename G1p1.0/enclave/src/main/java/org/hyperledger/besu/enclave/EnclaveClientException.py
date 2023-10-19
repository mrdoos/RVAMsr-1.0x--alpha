class EnclaveClientException(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code

    def get_status_code(self):
        return self.status_code
