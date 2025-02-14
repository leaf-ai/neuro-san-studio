from typing import Any
from typing import Dict
from typing import Union

from neuro_san.interfaces.coded_tool import CodedTool


class LightsSwitch(CodedTool):
    """
    CodedTool implementation that calls an API to turn lights on or off.
    """

    def __init__(self, lights_name: str):
        """
        Constructs a switch for lights.
        :param lights_name:
        """
        self.lights_name = lights_name
        print(f"... {lights_name} lights switch initialized ...")

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "desired_status": whether the lights should be turned ON or OFF.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
                but whose values are meant to be kept out of the chat stream.

                This dictionary is largely to be treated as read-only.
                It is possible to add key/value pairs to this dict that do not
                yet exist as a bulletin board, as long as the responsibility
                for which coded_tool publishes new entries is well understood
                by the agent chain implementation and the coded_tool implementation
                adding the data is not invoke()-ed more than once.

                Keys expected for this implementation are:
                    None

        :return:
            In case of successful execution:
                The URL to the app as a string.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """
        print(f">>>>>>>>>>>>>>>>>>> {self.lights_name} lights switch >>>>>>>>>>>>>>>>>>")
        message = f"{self.lights_name} lights switch pressed."
        print(message)
        print(">>>>>>>>>>>>>>>>>>>DONE !!!>>>>>>>>>>>>>>>>>>")
        return message