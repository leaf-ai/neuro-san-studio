from unittest import TestCase

from coded_tools.agentforce.agentforce_api import AgentforceAPI


class TestAgentforceAPI(TestCase):
    """
    Unit tests for AgentforceAPI class.
    """

    def test_invoke(self):
        """
        Tests the invoke method of the AgentforceAPI CodedTool.
        The AgentforceAPI CodedTool should query the Agentforce agent and return a response.
        Environment variables are NOT set for this test, so we expect the responses to be mocked.
        """
        agentforce_tool = AgentforceAPI()
        # Ask a first question
        inquiry_1 = "Can you give me a list of Lauren Bailey's most recent cases?"
        # Get the response
        response_1 = agentforce_tool.invoke(args={"inquiry": inquiry_1}, sly_data={})
        # Check the response contains the expected string.
        self.assertIn("Could you please provide Lauren Bailey's email address", response_1["response"])
        # Follow up with what Agentforce asked for. Session exists now, reuse it to continue the conversation instead
        # of starting a new one
        inquiry_2 = "lbailey@example.com"
        params = {"inquiry": inquiry_2,
                  "session_id": response_1["session_id"],
                  "access_token": response_1["access_token"]}
        response_2 = agentforce_tool.invoke(args=params, sly_data={})
        self.assertIn("It looks like there are no recent cases", response_2["response"])
        # Close the session
        agentforce_tool.agentforce.close_session(response_2["session_id"], response_2["access_token"])
