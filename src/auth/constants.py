from typing import Final


MIN_USERNAME_LENGTH: Final[int] = 5
MAX_USERNAME_LENGTH: Final[int] = 20
MIN_PASSWORD_LENGTH: Final[int] = 8
MAX_PASSWORD_LENGTH: Final[int] = 20
HASH_ALGORITHM: Final[str] = "HS256"
TOKEN_EXPIRES_AFTER: Final[int] = 60 * 60 * 24  # 1 day
