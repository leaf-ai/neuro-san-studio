import json
import os
from typing import Any
from typing import Dict

import requests
import uuid


# Einstein API URLs
AGENT_ID = "0XxKc000000kvtXKAQ"
BASE_URL = "https://api.salesforce.com/einstein/ai-agent/v1"
CLOSE_SESSION_URL = f"{BASE_URL}/sessions"
OPEN_SESSION_URL = f"{BASE_URL}/agents/{AGENT_ID}/sessions"
# Salesforce API URLs
SALESFORCE_URL = "https://mciardullo-cogfy26-225-demo.my.salesforce.com"
ACCESS_TOKEN_URL = f"{SALESFORCE_URL}/services/oauth2/token"


class AgentforceAdapter:
    """
    Adapter for the Agentforce API.
    This adapter allows to interact with the Agentforce API: create a session, post a message, close a session.
    """

    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Constructs a Salesforce Agentforce Adapter.
        :param client_id: the ID of the Agentforce client.
        :param client_secret: the secret of the Agentforce client.
        """
        # Get the client_id and client_secret from the environment variables if not provided
        if client_id is None:
            print("AgentforceAdapter: getting AGENTFORCE_CLIENT_ID from environment variables...")
            client_id = os.getenv("AGENTFORCE_CLIENT_ID", None)
            if client_id is None:
                print("AgentforceAdapter: AGENTFORCE_CLIENT_ID is NOT defined")
            else:
                print("AgentforceAdapter: client_id found in environment variables")
        if client_secret is None:
            print("AgentforceAdapter: getting AGENTFORCE_CLIENT_SECRET from environment variables...")
            client_secret = os.getenv("AGENTFORCE_CLIENT_SECRET", None)
            if client_secret is None:
                print("AgentforceAdapter: AGENTFORCE_CLIENT_SECRET is NOT defined")
            else:
                print("AgentforceAdapter: client_secret found in environment variables")

        if client_id is None or client_secret is None:
            print("ERROR: AgentforceAdapter is NOT configured. Please check your parameters or environment variables.")
            print("WARNING: Using mock responses.")
            # The service is not configured. We cannot query the API, but we can still use a mock response.
            self.is_configured = False
        else:
            # The service is configured. We can query the API.
            self.is_configured = True
            # Keep track of the params
            self.client_id = client_id
            self.client_secret = client_secret

    def create_session(self) -> (str, str):
        """
        Creates an Agentforce session.
        :return: a session id and an access token, as strings.
        """
        print("AgentforceAdapter: create_session called")
        # Get an access token
        access_token = self._get_access_token()
        session_id = self._get_session(access_token)
        print(f"    Session id: {session_id}")
        return session_id, access_token

    def _get_access_token(self) -> str:
        """
        Calls the Salesforce API to get an access token.
        :return: an access token, as a string.
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(ACCESS_TOKEN_URL, headers=headers, data=data)
        access_token = response.json()['access_token']
        return access_token

    @staticmethod
    def _get_session(access_token: str) -> str:
        """
        Calls the Salesforce API to get a session ID.
        :param access_token: an access token.
        :return: a session ID, as a string.
        """
        uuid_str = str(uuid.uuid4())
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        # print("----Session headers:")
        # print(headers)
        data = {
            "externalSessionKey": uuid_str,
            "instanceConfig": {
                "endpoint": SALESFORCE_URL
            },
            "streamingCapabilities": {
                "chunkTypes": ["Text"]
            },
            "bypassUser": "true"
        }
        # print("----Session data:")
        # print(data)
        # Convert data to json
        data_json = json.dumps(data)
        response = requests.post(OPEN_SESSION_URL, headers=headers, data=data_json)
        # print("---- Session:")
        # print(response.json())
        session_id = response.json()['sessionId']
        return session_id

    @staticmethod
    def close_session(session_id: str, access_token: str):
        """
        Closes an Agentforce session.
        :param session_id: the ID of the session to close.
        :param access_token: the corresponding access token.
        :return: Nothing
        """
        print("AgentforceAdapter: close_session called")
        close_session_url = f"{CLOSE_SESSION_URL}/{session_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-session-end-reason": "UserRequest",
        }
        requests.delete(close_session_url, headers=headers)
        print(f"    Session {session_id} closed:")

    def post_message(self, message: str, session_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Posts a message to the Agentforce API.
        Creates a new session if none is provided, along with its access_token.
        The session is what allows the Agentforce API to identify the conversation context and keep a conversation
        going.
        :param message: the message to post.
        :param session_id: the ID of the session to reuse to keep the conversation context, if any. If None,
        a new session will be created.
        :param access_token:the access token corresponding to the session_id. Can only be None if session_id is None.
        Creating new session will also create a new access token.
        :return: a dictionary containing:
        - session_id: the session id to use to continue the conversation,
        - access_token: the corresponding access_token
        - response: the response message from Agentforce.
        """
        if session_id in (None, "None"):
            session_id, access_token = self.create_session()
        message_url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{session_id}/messages"
        print(f"---- Message URL: {message_url}")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        timestamp = 42
        data = {
            "message": {
                "sequenceId": timestamp,
                "type": "Text",
                "text": message,
            },
            "variables": []
        }
        # Convert data to json
        data_json = json.dumps(data)
        print(f"---- Data JSON: {data_json}")
        response = requests.post(message_url, headers=headers, data=data_json)
        print(f"---- Response: {response}")
        print("---- Response JSON:")
        print(response.json())
        response_dict = {
            "session_id": session_id,
            "access_token": access_token,
            "response": response.json()
        }
        return response_dict


# Example usage:
if __name__ == "__main__":
    # Instantiate the AgentforceAdapter.
    # Client id and client secret are read from the environment variables.
    agentforce = AgentforceAdapter()
    # message = "Can you help me find training resources for Salesforce?"
    a_message = "Can you give me a list of Lauren Bailey's most recent cases?"
    print(f"USER: {a_message}")
    # Post the message to the Agentforce API
    a_response = agentforce.post_message(a_message)
    # Keep track of the session_id and access_token to continue the conversation
    a_session_id = a_response["session_id"]
    a_access_token = a_response["access_token"]
    a_response_message = a_response["response"]["messages"][0]["message"]
    print(f"AGENTFORCE: {a_response_message}")
    a_second_message = "lbailey@example.com"
    print(f"USER: {a_second_message}")
    # Continue the conversation by using the session_id and access_token
    a_second_response = agentforce.post_message(a_second_message, a_session_id, a_access_token)
    a_second_response_message = a_second_response["response"]["messages"][0]["message"]
    print(f"AGENTFORCE: {a_second_response_message}")
    # Close the session
    agentforce.close_session(a_session_id, a_access_token)
    print("Done!")
