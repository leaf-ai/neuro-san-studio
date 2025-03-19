from typing import Any
from typing import Dict
from typing import Union
import json

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.agentforce.agentforce_adapter import AgentforceAdapter

MOCK_RESPONSE = \
"""
{'messages': [{'type': 'Inform', 'id': 'af4b0a83-5f32-4fa0-9f78-22c1a3522ba3', 'feedbackId': 'b8058c93-d3a4-4586-b83c-ceff44bb2a46', 'planId': 'b8058c93-d3a4-4586-b83c-ceff44bb2a46', 'isContentSafe': True, 'message': "Here are Lauren Bailey's most recent cases:\n\n1. Subject: Cognizant Test Case\n   - Status: New\n2. Subject: Question on products\n   - Status: New\n3. Subject: I have a product suggestion.\n   - Status: Closed\n4. Subject: I have a question about my bill\n   - Status: New\n5. Subject: Can you expedite my order?\n   - Status: Closed\n\nIf you need more details or assistance with any of these cases, just let me know!", 'result': [], 'citedReferences': []}], '_links': {'self': None, 'messages': {'href': 'https://api.salesforce.com/einstein/ai-agent/v1/sessions/e3a973c5-e4ad-44af-b43f-4a23601516cf/messages'}, 'messagesStream': {'href': 'https://api.salesforce.com/einstein/ai-agent/v1/sessions/e3a973c5-e4ad-44af-b43f-4a23601516cf/messages/stream'}, 'session': {'href': 'https://api.salesforce.com/einstein/ai-agent/v1/agents/0XxKc000000kvtXKAQ/sessions'}, 'end': {'href': 'https://api.salesforce.com/einstein/ai-agent/v1/sessions/e3a973c5-e4ad-44af-b43f-4a23601516cf'}}}"
"""

class AgentforceAPI(CodedTool):
    """
    CodedTool implementation of Agentforce API.
    """

    def __init__(self):
        """
        Constructs an Agentforce API for Cognizant's Neuro AI Multi-Agent Accelerator.
        """
        # Construct an AgentforceAdapter object using environment variables
        self.agentforce = AgentforceAdapter(None, None)

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent. This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "inquiry" the date on which to check the balances (format: 'YYYY-MM-DD')

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
                A response from the Agentforce API.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """
        inquiry: str = args.get("inquiry")
        # final_response: Dict[str, Any] = {}
        tool_name = self.__class__.__name__
        print(f"========== Calling {tool_name} ==========")
        print(f"Inquiry: {inquiry}")
        if self.agentforce.is_configured:
            print("AgentforceAdapter is configured. Fetching response...")
            res = self.agentforce.post_message(inquiry)
        else:
            print("WARNING: AgentforceAdapter is not configured. Using mock response")
            res = "This is amock response"
        res = json.dumps(res)
        message_list = json.loads(res).get("messages", "No messages received")
        final_response = message_list[0].get("message", "No message received")
        # final_response["message"] = message_list[0].get("message", "No message received")
        # final_response["app_name"] = tool_name
        print("-----------------------")
        print("Agentforce response: ", final_response)
        print(f"========== Done with {tool_name} ==========")
        return final_response


# Example usage:
if __name__ == "__main__":
    agentforce_tool = AgentforceAPI()

    af_inquiry = "find training resources for Salesforce"
    # Get response
    af_res = agentforce_tool.invoke(args={"inquiry": af_inquiry}, sly_data={})
