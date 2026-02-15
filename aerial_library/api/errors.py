from aerial_library.api.feature import Feature


class AerialLibraryError(Exception):
    pass


class InvalidCrazyflieAddress(AerialLibraryError):
    def __init__(self, address: str):
        super().__init__(
            f"Invalid Crazyflie address: '{address}'."
            f" The address must contain exactly 10 hexadecimal digits."
            f" Example address: 'E7E7E7E7E7'"
        )


class CrazyflieNotFound(AerialLibraryError):
    def __init__(self, address: str):
        super().__init__(
            f"Could not find a Crazyflie with address '{address}'."
            f" Is the radio or USB cable connected?"
            f" Is the drone turned on?"
        )


class RequiredDeckNotFound(AerialLibraryError):
    def __init__(self, deck_name: str):
        super().__init__(
            f"The {deck_name} Deck is required, but it was not detected on the drone."
            f" Is it attached?"
            f" Is it attached the right way around?"
        )


class AlreadyConnected(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone was already connected, cannot connect again")


class AlreadyDisconnected(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone is not connected, cannot disconnect")


class MissingFeature(AerialLibraryError):
    def __init__(self, feature: Feature):
        super().__init__(
            f"The {feature} feature is required to do this,"
            f" but it was not specified when creating the drone"
        )


class AlreadyFlying(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone was already flying, cannot take off again")


class AlreadyLanded(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone is not flying, cannot land")


class CannotMoveOnGround(AerialLibraryError):
    def __init__(self):
        super().__init__("The drone cannot move on the ground, it must take off first")
