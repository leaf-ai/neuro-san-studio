from typing import Any
from typing import Dict
from typing import Union
import json

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.agentforce.agentforce_adapter import AgentforceAdapter

MOCK_RESPONSE_1 = \
"""
{"messages": [{"type": "Inform", "id": "04d35a5d-6011-4eb9-88a9-2897f49a6bdc", "feedbackId": "7d92a297-dc95-4306-b638-42f6e36ddfab", "planId": "7d92a297-dc95-4306-b638-42f6e36ddfab", "isContentSafe": true, "message": "Sure, I can help with that. Could you please provide Lauren Bailey's email address to look up her cases?", "result": [], "citedReferences": []}], "_links": {"self": null, "messages": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/06518755-b897-4311-afea-2aab1df77314/messages"}, "messagesStream": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/06518755-b897-4311-afea-2aab1df77314/messages/stream"}, "session": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/agents/0XxKc000000kvtXKAQ/sessions"}, "end": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/06518755-b897-4311-afea-2aab1df77314"}}}
"""
MOCK_RESPONSE_2 = \
"""
{"messages": [{"type": "Inform", "id": "caf90c84-a150-4ccd-8430-eb29189696ac", "feedbackId": "e24505db-1edd-4b76-b5f5-908be083fc67", "planId": "e24505db-1edd-4b76-b5f5-908be083fc67", "isContentSafe": true, "message": "It looks like there are no recent cases associated with Lauren Bailey's email address. Is there anything else I can assist you with?", "result": [], "citedReferences": []}], "_links": {"self": null, "messages": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/06518755-b897-4311-afea-2aab1df77314/messages"}, "messagesStream": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/06518755-b897-4311-afea-2aab1df77314/messages/stream"}, "session": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/agents/0XxKc000000kvtXKAQ/sessions"}, "end": {"href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/06518755-b897-4311-afea-2aab1df77314"}}}
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
                    "inquiry": the user request to the Agentforce API, as a string.

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
        # Parse arguments
        inquiry: str = args.get("inquiry")
        session_id: str = args.get("session_id", None)
        access_token: str = args.get("access_token", None)

        tool_name = self.__class__.__name__
        print(f"========== Calling {tool_name} ==========")
        print(f"Inquiry: {inquiry}")
        print(f"Session ID: {session_id}")
        print(f"Access Token: {access_token}")

        if self.agentforce.is_configured:
            print("AgentforceAdapter is configured. Fetching response...")
            res = self.agentforce.post_message(inquiry)
        else:
            print("WARNING: AgentforceAdapter is NOT configured. Using a mock response")
            if session_id is None:
                # No session yet. This is the first request the user makes
                res = json.loads(MOCK_RESPONSE_1)
            else:
                # The user has a session. This is a follow-up request
                res = json.loads(MOCK_RESPONSE_2)
        message_list = res.get("messages", "No messages received")
        final_response = message_list[0].get("message", "No message received")
        print("-----------------------")
        print("Agentforce response: ", final_response)
        print(f"========== Done with {tool_name} ==========")
        return final_response


# Example usage:
if __name__ == "__main__":
    agentforce_tool = AgentforceAPI()

    af_inquiry = "Can you give me a list of Lauren Bailey's most recent cases?"
    # Get response
    af_res = agentforce_tool.invoke(args={"inquiry": af_inquiry}, sly_data={})
    # Follow up - session exists now
    af_inquiry = "lbailey@example.com"
    params = {"inquiry": af_inquiry,
              "session_id": "06518755-b897-4311-afea-2aab1df77314",
              "access_token": "1234567890"}
    af_res_2 = agentforce_tool.invoke(args=params, sly_data={})
