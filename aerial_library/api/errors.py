from aerial_library.api.feature import Feature


class AerialLibraryError(Exception):
    pass


class MissingFeature(AerialLibraryError):
    def __init__(self, feature: Feature):
        super().__init__(
            f"The {feature} feature is required to do this, but it was not specified"
        )


class NoCrazyflieFound(AerialLibraryError):
    def __init__(self):
        super().__init__("Could not find any Crazyflie to connect to")


class InvalidCrazyflieAddress(AerialLibraryError):
    def __init__(self, address: str):
        super().__init__(
            f"Invalid Crazyflie address: '{address}'. Example address: 'E7E7E7E7E7'"
        )


class FlowDeckNotFound(AerialLibraryError):
    def __init__(self):
        super().__init__(
            "The Flow Deck is required, but it was not found. Is it attached?"
        )


class MultiRangerDeckNotFound(AerialLibraryError):
    def __init__(self):
        super().__init__(
            "The Multi-ranger Deck is required, but it was not found. Is it attached?"
        )


class AlreadyConnected(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone is already connected, cannot connect again")


class NotConnected(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone is not connected, cannot disconnect")


class AlreadyFlying(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone is already flying, cannot take off again")


class AlreadyLanded(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone is not flying, cannot land")


class CannotMoveOnGround(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone cannot move now, it is not flying")
