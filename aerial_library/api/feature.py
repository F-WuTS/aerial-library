from enum import Enum


class Feature(Enum):
    FlowDeck = "Flow Deck"
    MultiRangerDeck = "Multi Ranger Deck"
    FastMode = "Fast Mode"


FlowDeck = Feature.FlowDeck
"""Specify this feature to use the Flow Deck on your drone.

This enables the use of the `move` API.
"""


MultiRangerDeck = Feature.MultiRangerDeck
"""Specify this feature to use the Flow Deck on your drone.

This enables the use of the `measure` API.
"""


FastMode = Feature.FastMode
"""Specify this feature to make your drone move a lot faster.

Note that takeoff and landing speeds remain unchanged.
"""
