from enum import Enum


class Feature(Enum):
    FlowDeck = "Flow Deck"
    MultiRangerDeck = "Multi-ranger Deck"

    def __str__(self) -> str:
        return self.name


FlowDeck = Feature.FlowDeck
MultiRangerDeck = Feature.MultiRangerDeck
