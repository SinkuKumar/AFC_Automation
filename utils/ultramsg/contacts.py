"""
Ultramsg Contacts
-------------------

This module provides functionality to interact with contacts
    with the help of Ultramsg WhatsApp API.

This module can be used as a standalone script, 
if that the `UMSG_INSTANCE_ID` and `UMSG_SECRET_KEY` environment variables are set.

:module: contacts.py
:platform: Unix, Windows

:date: March 3, 2025
:author: Niladri Mallik `niladrimallik.p@hq.graphxsys.com <mailto:niladrimallik.p@hq.graphxsys.com>`

# TODO: Implement logging
# TODO: Add error handling
# TODO: Implement error codes
"""

import os
import sys

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.ultramsg.base import UltraMsgBase

class UltraMsgContacts:
    """
    Child class inherits UltraMsgBase class.
    Implements methods to deal with messages in WhatsApp using the API.\n
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def block_contact(self, chat_id: str):
        '''
        Block contact on WhatsApp for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = "contacts/block",
                                           payload = payload, request_type = "POST")

    def unblock_contact(self, chat_id: str):
        '''
        Unblock contact on WhatsApp for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = "contacts/unblock",
                                           payload = payload, request_type = "POST")

    def contact_list(self):
        '''
        Get the contacts list.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "contacts",
                                           payload = query_string, request_type = "GET")

    def contact_ids(self, clear: bool):
        '''
        Get the contact IDs.
        Uses GET request.

        :param clear:
        :type clear: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "clear" : clear
        }
        return self.umsg_base.make_request(url = "contacts/ids",
                                           payload = query_string, request_type = "GET")

    def contact_info(self, chat_id: str):
        '''
        Get the contact info for the given chat ID.
        Uses GET request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chat_id
        }
        return self.umsg_base.make_request(url = "contacts/contact",
                                           payload = query_string, request_type = "GET")

    def blocked_contacts(self):
        '''
        Get all blocked contacts.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "contacts/blocked",
                                           payload = query_string, request_type = "GET")

    def invalid_contacts(self, clear: bool):
        '''
        Get all invalid contacts.
        Uses GET request.

        :param clear: 
        :type clear: bool
        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "clear" : clear
        }
        return self.umsg_base.make_request(url = "contacts/invalid",
                                           payload = query_string, request_type = "GET")

    def check_if_whatsapp_user(self, chat_id: str, nocache: bool = False):
        '''
        Checks if user is WhatsApp user
        Uses GET request.

        :param chatId: chatId for contact or group.
        :type chatId: str
        :param nocache: Whether to check the contacts cache or not.
            Contact information is normally cached for 3 days. 
            Setting the nocache parameter to `True` bypasses the cache ensuring check is performed.
        :type nocache: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chat_id,
            "nocache" : nocache
        }
        return self.umsg_base.make_request(url = "contacts/check",
                                           payload = query_string, request_type = "GET")

    def contact_profile_picture(self, chat_id: str):
        '''
        Get the contact profile picture for the given chat ID.
        Uses GET request.

        :param chatId: chatId for contact.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chat_id
        }
        return self.umsg_base.make_request(url = "contacts/image",
                                           payload = query_string, request_type = "GET")

if __name__ == '__main__':
    # TODO: Remove this in production
    try:
        import os

        from dotenv import load_dotenv

        # TODO: Remove this later
        load_dotenv()

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgContacts(um_base)
    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")
