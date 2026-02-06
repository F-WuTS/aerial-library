from aerial_library.api.feature import Feature


class AerialLibraryError(Exception):
    pass


class MissingFeature(AerialLibraryError):
    def __init__(self, feature: Feature, api_name: str):
        super().__init__(f"{feature} is required to use the '{api_name}' API")


class NoCrazyflieFound(AerialLibraryError):
    def __init__(self):
        super().__init__("Could not find any Crazyflie to connect to")


class FlowDeckNotFound(AerialLibraryError):
    def __init__(self):
        super().__init__("Flow deck not found, is it attached?")


class MultiRangerDeckNotFound(AerialLibraryError):
    def __init__(self):
        super().__init__("MultiRanger deck not found, is it attached?")


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
