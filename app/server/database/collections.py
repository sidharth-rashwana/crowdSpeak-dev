from enum import Enum


class Collections(str, Enum):
    ACCOUNTS = 'accounts'
    MESSAGES = 'messages'
    CHANNELS = 'channels'
