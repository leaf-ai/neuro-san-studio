from coded_tools.smart_home_onf.lights_switch import LightsSwitch


class LivingRoomLightsSwitch(LightsSwitch):
    """
    CodedTool implementation that calls an API to turn lights on or off.
    """

    def __init__(self):
        """
        Constructs a switch for living room lights.
        """
        super().__init__("Living room")
