from enum import Enum


class Feature(Enum):
    FlowDeck = "Flow Deck"
    MultiRangerDeck = "Multi Ranger Deck"


FlowDeck = Feature.FlowDeck
"""Specify this feature to use the Flow Deck on your drone.

This enables the use of the `move` API.
"""


MultiRangerDeck = Feature.MultiRangerDeck
"""Specify this feature to use the Flow Deck on your drone.

This enables the use of the `measure` API.
"""
