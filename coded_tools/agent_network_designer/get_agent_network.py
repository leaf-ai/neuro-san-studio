from typing import Any
from typing import Dict
from typing import Union

import logging

from neuro_san.interfaces.coded_tool import CodedTool

AGENT_NETWORK_NAME = "AutomaticallyDesignedAgentNetwork"

class GetAgentNetwork(CodedTool):
    """
    CodedTool implementation which provides a way to get an outline of an agent network stored in sly data
    """

    def __init__(self):
        self.agents = None

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "app_name" the name of the One Cognizant app for which the URL is needed.

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
                The full agent network as a string.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """
        self.agents = sly_data.get(AGENT_NETWORK_NAME, None)
        if not self.agents:
            return "Error: No network in sly data!"
        logger = logging.getLogger(self.__class__.__name__)
        logger.info(">>>>>>>>>>>>>>>>>>>GetAgentNetwork>>>>>>>>>>>>>>>>>>")
        the_agent_network_str = str(self.agents)
        logger.info("The resulting agent network: \n %s", str(the_agent_network_str))
        logger.info(">>>>>>>>>>>>>>>>>>>DONE !!!>>>>>>>>>>>>>>>>>>")
        return the_agent_network_str
