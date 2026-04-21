"""
用户相关异常
"""


class UserException(Exception):
    """用户异常基类"""
    pass


class UserNotFoundError(UserException):
    """用户未找到异常"""
    pass


class UserAlreadyExistsError(UserException):
    """用户已存在异常"""
    pass


class InvalidCredentialsError(UserException):
    """无效凭证异常"""
    pass


class UserInactiveError(UserException):
    """用户未激活异常"""
    pass
