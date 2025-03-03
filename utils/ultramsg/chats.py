"""
Ultramsg Chats
-------------------

This module provides functionality to interact with chats
    with the help of Ultramsg WhatsApp API.

This module can be used as a standalone script, 
if that the `UMSG_INSTANCE_ID` and `UMSG_SECRET_KEY` environment variables are set.

:module: chats.py
:platform: Unix, Windows

:date: March 3, 2025
:author: Niladri Mallik `niladrimallik.p@hq.graphxsys.com <mailto:niladrimallik.p@hq.graphxsys.com>`

# TODO: Implement logging
# TODO: Add error handling
# TODO: Implement error codes
"""

import sys
import os

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.ultramsg.base import UltraMsgBase

class UltraMsgChats:
    """
    Child class inherits UltraMsgBase class.
    Implements methods to deal with chats in WhatsApp using the API.\n
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def chat_list(self):
        '''
        Get list of chats.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        # query_string = {"token" : f'{self.umsg_base.token}'}
        return self.umsg_base.make_request(url = "chats",
                                           payload = None, request_type = "GET")

    def chat_ids(self, clear: bool):
        '''
        Get the chat IDs.
        Uses GET request.

        :param clear:
        :type clear: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"clear" : clear}
        return self.umsg_base.make_request(url = "chats/ids",
                                           payload = query_string, request_type = "GET")

    def last_message(self, chat_id: str, limit: int):
        '''
        Get last message from chat conversation for the given chat ID.
        Uses GET request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :param limit: number of messages per request, max value: 1000
        :type limit: int

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "chatId" : chat_id,
            "limit" : limit
        }
        return self.umsg_base.make_request(url = "chats/messages",
                                           payload = query_string, request_type = "GET")

    def archive_chats(self, chat_id: str):
        '''
        Archives the chat for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = 'chats/archive',
                                           payload = payload, request_type = "POST")

    def unarchive_chats(self, chat_id: str):
        '''
        Uarchives the chat for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = 'chats/unarchive',
                                           payload = payload, request_type = "POST")

    def clear_messages(self, chat_id: str):
        '''
        Clears all messages from the chat for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = 'chats/clearMessages',
                                           payload = payload, request_type = "POST")

    def delete_chat(self, chat_id: str):
        '''
        Deletes the chat from chat list for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = 'chats/delete',
                                           payload = payload, request_type = "POST")

    def mark_chat_read(self, chat_id: str):
        '''
        Marks chat message as read for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chat_id}"
        return self.umsg_base.make_request(url = 'chats/read',
                                           payload = payload, request_type = "POST")

if __name__ == "__main__":
    try:
        import os

        from dotenv import load_dotenv

        load_dotenv()

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_chats = UltraMsgChats(um_base)

        # last_msg_resp = um_chats.last_message('919674573242@c.us', 1)
        # print(last_msg_resp)

        print(f'Get chat IDs: {um_chats.chat_ids(True)}')

        print(um_chats.chat_list())

    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")
