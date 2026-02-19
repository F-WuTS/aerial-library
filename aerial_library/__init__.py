"""
Python library for the robo4you Aerial Junior Challenge.

Enables simple, intuitive interaction with the Crazyflie 2.1 drone.

To get started, please see the user guide in the downloads section of our website:
https://aerial-challenge.org/downloads/
"""

from aerial_library.api.drone import Drone
from aerial_library.api.actions import Actions
from aerial_library.api.feature import FlowDeck, MultiRangerDeck

__all__ = [
    "Drone",
    "Actions",
    "FlowDeck",
    "MultiRangerDeck",
]
