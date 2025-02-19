import requests
from typing import Dict, Any, Union
from neuro_san.interfaces.coded_tool import CodedTool

class SmartHomeAPIKitchenLightTool(CodedTool):
    """
    CodedTool implementation that calls an API to control the Kitchen Lights.
    """
    def __init__(self):
        """
        Constructor for the api.
        """
        self.base_http_url = "http://127.0.0.1:8001/api/v1/"

    def get_status_http(self) -> Union[str, Dict[str, Any]]:
        endpoint = self.base_http_url + "kitchenlight/status"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()  # Expected: {"kitchenlight": true/false}
        except Exception as e:
            return f"Error retrieving kitchen lights status via HTTP: {str(e)}"

    def set_state_http(self, desired_state: str) -> Union[str, Dict[str, Any]]:
        current_status = self.get_status_http()
        if isinstance(current_status, dict) and "kitchenlight" in current_status:
            current_state = "on" if current_status["kitchenlight"] else "off"
            if current_state == desired_state:
                return f"Kitchen lights are already {desired_state}."
        endpoint = self.base_http_url + "kitchenlight"
        payload = {"state": desired_state}
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error setting kitchen lights state via HTTP: {str(e)}"

    def handle_toggle(self, action: str) -> Union[str, Dict[str, Any]]:
        return self.set_state_http(action)

    def handle_status(self, action: str) -> Union[str, Dict[str, Any]]:
        return self.get_status_http()

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[str, Dict[str, Any]]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "action": what the user wants to do with the device: On or Off or check Status or Info.

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
                The response for the given action.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """
        action = args.get("action", "status").lower()
        print(f"**********Calling {self.__class__.__name__} API**********")
        print(f"With action: {action}")
        if not action:
            return "Error: No action provided."
        action_map = {
            "on": self.handle_toggle,
            "off": self.handle_toggle,
            "status": self.handle_status,
            "info": self.handle_status
        }
        if action not in action_map:
            return "Error: Unknown action. Use 'on', 'off', 'status', or 'info'."
        res = action_map[action](action)
        print(f"********** {self.__class__.__name__} API Action completed **********")
        return {"response": res}
