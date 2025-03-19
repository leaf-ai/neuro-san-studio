import os
import requests


class AgentforceAdapter:
    """
    Absence Manager for Cognizant's OneCognizant intranet.
    """
    ACCESS_TOKEN_URL = "https://mciardullo-cogfy26-225-demo.my.salesforce.com/services/oauth2/token"
    BASE_URL = "https://apigatewaysit.cognizant.com/1CPlatform"
    APP_URL = "https://compass.talent.cognizant.com/psc/HCMPRD/EMPLOYEE/HRMS/c/CT_FLUID_MNU.CT_ESS_MABS_FLU.GBL"

    def __init__(self, client_id, client_secret):
        """
        Constructs an Absence Manager for Cognizant's OneCognizant intranet.
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
            print(f"Access token: {self.access_token}")
            # Set the headers
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'SourceType': 'Web'
            }

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

    def get_absence_types(self, start_date):
        """
        Get absence types.
        URL: /hcm/leave/details
        :param start_date: The start date for the absence types (format: 'YYYY-MM-DD').
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/hcm/leave/details"
        payload = {
            "Start_date": start_date
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def get_absence_details(self, start_date, end_date, abs_pin, partial_days, absence_reason): # /hcm/leave/selection
        """
        Get absence details.

        :param start_date: Start date (format: 'YYYY-MM-DD').
        :param end_date: End date (format: 'YYYY-MM-DD').
        :param abs_pin: Absence PIN.
        :param partial_days: Partial days.
        :param absence_reason: Absence reason.
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/hcm/leave/selection"
        payload = {
        "Start_date": start_date,
        "End_date": end_date,
        "Abs_pin": abs_pin,
        "Partial_days": partial_days,
        "Absence_Reason": absence_reason
    }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()


# Example usage:
if __name__ == "__main__":
    a_client_id = None  # Replace with your client_id
    a_client_secret = None  # Replace with your client_id
    agentforce = AgentforceAdapter(a_client_id, a_client_secret)
