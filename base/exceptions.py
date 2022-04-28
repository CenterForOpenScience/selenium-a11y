class PageException(Exception):
    pass


class HttpError(PageException):
    pass


class LoginError(PageException):
    """Error used when driver is in an unexpected login state."""

    pass
