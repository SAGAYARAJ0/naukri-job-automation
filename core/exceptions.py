"""
Custom exceptions for Naukri job automation system.
"""


class NaukriAutomationException(Exception):
    """Base exception for all automation errors."""
    pass


class LoginException(NaukriAutomationException):
    """Raised when login fails."""
    pass


class CaptchaRequiredException(LoginException):
    """Raised when CAPTCHA appears during login."""
    pass


class SessionExpiredException(NaukriAutomationException):
    """Raised when session expires."""
    pass


class SearchException(NaukriAutomationException):
    """Raised when job search fails."""
    pass


class FilterException(NaukriAutomationException):
    """Raised when job filtering fails."""
    pass


class ApplyException(NaukriAutomationException):
    """Raised when job application fails."""
    pass


class AlreadyAppliedException(ApplyException):
    """Raised when already applied to job."""
    pass


class ExternalRedirectException(ApplyException):
    """Raised when apply redirects to external site."""
    pass


class StorageException(NaukriAutomationException):
    """Raised when storage operations fail."""
    pass


class ConfigException(NaukriAutomationException):
    """Raised when configuration is invalid."""
    pass


class DriverException(NaukriAutomationException):
    """Raised when WebDriver operations fail."""
    pass


class TimeoutException(NaukriAutomationException):
    """Raised when operation exceeds timeout."""
    pass


class RateLimitException(NaukriAutomationException):
    """Raised when rate limited by server."""
    pass
