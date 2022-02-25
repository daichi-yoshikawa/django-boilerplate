from rest_framework.exceptions import APIException


class DataAlreadyRegistered(APIException):
  def __init__(self, detail='Data already registered', code=None):
    super().__init__(detail=detail, code=code)


class EmailNotRegistered(APIException):
  def __init__(self, detail='Data already registered', code=None):
    super().__init__(detail=detail, code=code)


class EmailVerificationCodeExpired(APIException):
  def __init__(self, detail='Verification code is expired.', code=None):
    super().__init__(detail=detail, code=code)


class LoginAttemptLimitError(APIException):
  def __init__(self, detail='Too many login attempt.', code=None):
    super().__init__(detail=detail, code=code)


class OwnershipError(APIException):
  def __init__(self, detail='Request from wrong user.', code=None):
    super().__init__(detail=detail, code=code)


class PasswordResetCodeExpired(APIException):
  def __init__(self, detail='Password reset code is expired.', code=None):
    super().__init__(detail=detail, code=code)


class RequestSizeError(APIException):
  def __init__(self, detail='Request size is invalid.', code=None):
    super().__init__(detail=detail, code=code)


class TenantInvitationCodeExpired(APIException):
  def __init__(self, detail='Invitation code is expired.', code=None):
    super().__init__(detail=detail, code=code)
