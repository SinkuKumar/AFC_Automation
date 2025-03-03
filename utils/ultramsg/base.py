"""
Ultramsg Base 
-------------------

This module provides functionality to interact with the UltraMsg API to send messages via WhatsApp.

`UltraMsgBase` class initializes an UltraMsg instance with an `instance_id`
and `token`, and a method to send requests to the UltraMsg API.

This module can be used as a standalone script to send a WhatsApp message, 
    if that the `UMSG_INSTANCE_ID` and `UMSG_SECRET_KEY` environment variables are set.

:module: ultramsg.base.py
:platform: Unix, Windows

:date: March 3, 2025
:author: Niladri Mallik `niladrimallik.p@hq.graphxsys.com <mailto:niladrimallik.p@hq.graphxsys.com>`

# TODO: Implement logging
# TODO: Add error handling
# TODO: Implement error codes
"""

import logging
import requests

class UltraMsgBase:
    """
    A class to represent an UltraMsg instance for WhatsApp communication.

    This class sends requests to the UltraMsg API using the provided instance ID and token.
    The instance is initialized with the `instance_id` and `token`.
    It constructs the base URL for making requests to the UltraMsg API.

    Attributes:
        instance_id (str): The instance ID provided by UltraMsg.
        token (str): The secret API token for authentication with the UltraMsg API.
        url (str): The base URL for the UltraMsg API, constructed using the instance ID.
    """

    def __init__(self, instance_id: str, token: str):
        """
        Initializes the UltraMsg instance with instance ID and token for communication.

        :param instance_id: The unique identifier for the UltraMsg instance.
        :type instance_id: str
        :param token: The secret key for authenticating API requests.
        :type token: str
        """
        self.instance_id = instance_id
        self.token = token
        self.url = f'https://api.ultramsg.com/{self.instance_id}'

    def make_request(self, url: str, payload: str, request_type: str = 'POST') -> str:
        """
        Makes a request to the UltraMsg server with the provided payload and request type.

        This method constructs the full URL, prepares the payload, and sends the request to the UltraMsg API.

        :param url: The endpoint path to make the request to (e.g., 'messages/chat').
        :type url: str
        :param payload: The parameters to be sent as the request payload (formatted as a query string).
        :type payload: str
        :param request_type: The HTTP method to use for the request (either 'GET' or 'POST'). Defaults to 'POST'.
        :type request_type: str
        :returns: The response content from the UltraMsg server, typically a JSON string.
        :rtype: str
        """
        self.req_url = f'{self.url}/{url}'
        self.payload = f'token={self.token}&{payload}'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request(request_type, self.req_url, 
                                    data=self.payload, headers=self.headers)
        return response.text

if __name__ == "__main__":
    # Example usage
    import os
    from dotenv import load_dotenv

    load_dotenv()

    instance_id = os.getenv("UMSG_INSTANCE_ID")
    token = os.getenv("UMSG_SECRET_KEY")
    ultra_msg = UltraMsgBase(instance_id, token)

    TEST_PHONE = '919717425826'
    TEST_SYMBOL = 'Hello, this is a test message!'
    payload = f'to={TEST_PHONE}&body={TEST_SYMBOL}'

    msg_resp = ultra_msg.make_request('messages/chat', payload, 'POST')
    print(msg_resp)
