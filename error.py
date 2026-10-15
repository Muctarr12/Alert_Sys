class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""


class APIError(Exception):
    """Raised when an API request fails."""


class APIResponseError(APIError):
    """Raised when an API response cannot be parsed or lacks expected data."""