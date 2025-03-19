import json
import os
import requests
import uuid


class AgentforceAdapter:
    """
    Absence Manager for Cognizant's OneCognizant intranet.
    """
    ACCESS_TOKEN_URL = "https://mciardullo-cogfy26-225-demo.my.salesforce.com/services/oauth2/token"
    SESSION_URL = "https://api.salesforce.com/einstein/ai-agent/v1/agents/0XxKc000000kvtXKAQ/sessions"

    def __init__(self, client_id, client_secret):
        """
        Constructs a Salesforce Agentforce Adapter.
        @param client_id: The API client ID.
        @param client_secret: The API client secret.
        @param associate_id: an associate ID.
        """

        # Get the client_id, client_secret, and associate_id from the environment variables
        if client_id is None:
            print("AgentforceAdapter: no client_id provided, checking environment variables")
            client_id = os.getenv("AGENTFORCE_CLIENT_ID", None)
            if client_id is None:
                print("AgentforceAdapter: AGENTFORCE_CLIENT_ID is NOT defined")
            else:
                print("AgentforceAdapter: client_id found in environment variables")
        if client_secret is None:
            print("AgentforceAdapter: no client_secret provided, checking environment variables")
            client_secret = os.getenv("AGENTFORCE_CLIENT_SECRET", None)
            if client_secret is None:
                print("AgentforceAdapter: AGENTFORCE_CLIENT_SECRET is NOT defined")
            else:
                print("AgentforceAdapter: client_secret found in environment variables")

        if client_id is None or client_secret is None:
            print("ERROR: AgentforceAdapter is NOT configured. Please check your parameters or environment variables.")
            # The service is not configured. We cannot query the API, but we can still use a mock response.
            self.is_configured = False
        else:
            # The service is configured. We can query the API.
            self.is_configured = True
            # Keep track of the params
            self.client_id = client_id
            self.client_secret = client_secret
            # Set the headers to get the access token

            # Get an access token
            self.access_token = self.get_access_token()
            # print(f"Access token: {self.access_token}")
            # Set the headers
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'SourceType': 'Web'
            }
            uuid_str = str(uuid.uuid4())
            self.session_id = self.get_session(uuid_str)

    def get_access_token(self):
        """
        Get the access token.
        @return: and access token
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(AgentforceAdapter.ACCESS_TOKEN_URL, headers=headers, data=data)
        access_token = response.json()['access_token']
        return access_token

    def get_session(self, uuid_str):
        """
        Get a session
        @return: a session
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        # print("----Session headers:")
        # print(headers)
        data = {
            "externalSessionKey": uuid_str,
            "instanceConfig": {
                "endpoint": "https://mciardullo-cogfy26-225-demo.my.salesforce.com"
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
        response = requests.post(AgentforceAdapter.SESSION_URL, headers=headers, data=data_json)
        # print("---- Session:")
        # print(response.json())
        session_id = response.json()['sessionId']
        print("---- Session_id: ", session_id)
        return session_id

    def close_session(self):
        close_session_base_url = "https://api.salesforce.com/einstein/ai-agent/v1/sessions"
        close_session_url = f"{close_session_base_url}/{self.session_id}"
        print(f"---- Close session URL: {close_session_url}")
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "x-session-end-reason": "UserRequest",
        }
        response = requests.delete(close_session_url, headers=headers)
        print(response)
        print("---- Session closed:")

    def post_message(self, message):
        message_url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{self.session_id}/messages"
        print(f"---- Message URL: {message_url}")
        headers = {
            "Authorization": f"Bearer {self.access_token}",
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
        print("---- Response:")
        print(response)
        print("---- Response JSON:")
        print(response.json())
        return response.json()


# Example usage:
if __name__ == "__main__":
    a_client_id = None  # Replace with your client_id
    a_client_secret = None  # Replace with your client_id
    agentforce = AgentforceAdapter(a_client_id, a_client_secret)
    # message = "Can you help me find training resources for Salesforce?"
    a_message = "Can you give me a list of Lauren Bailey's most recent cases?"
    agentforce.post_message(a_message)
    a_second_message = "lbailey@example.com"
    agentforce.post_message(a_second_message)
    agentforce.close_session()
    print("Done!")
