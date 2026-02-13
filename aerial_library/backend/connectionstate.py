from enum import Enum


class ConnectionState(Enum):
    Disconnected = 0
    Connecting = 1
    Connected = 2
    Disconnecting = 3
