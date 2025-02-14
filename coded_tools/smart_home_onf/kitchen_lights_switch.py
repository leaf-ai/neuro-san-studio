from coded_tools.smart_home_onf.lights_switch import LightsSwitch


class KitchenLightsSwitch(LightsSwitch):
    """
    CodedTool implementation that calls an API to turn lights on or off.
    """

    def __init__(self):
        """
        Constructs a switch for kitchen lights.
        """
        super().__init__("Kitchen")
