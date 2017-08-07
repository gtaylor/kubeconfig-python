class KubeConfigError(Exception):
    """Top-level base class for all module exceptions."""

    pass


class KubectlNotFoundError(KubeConfigError):
    """Raised when the Kubectl executable is not found on the path."""

    def __init__(self):
        super().__init__("Could not find kubectl on the path.")


class KubectlCommandError(KubeConfigError):
    """Raised when kubectl exit(1)'s or returns an error line."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)
