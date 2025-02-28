import sys
import os
from dotenv import load_dotenv

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils_ultraMsg.ultramsg_base import UltraMsgBase

class UltraMsgChats:
    """
    Child class inherits UltraMsgBase class and implements methods to deal with messages in WhatsApp using the API.\n
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
        return self.umsg_base.make_request(url = "chats", payload = None, type = "GET")
    
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
        return self.umsg_base.make_request(url = "chats/ids", payload = query_string, type = "GET")
    
    def last_message(self, chatId: str, limit: int):
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
            "chatId" : chatId,
            "limit" : limit
        }
        return self.umsg_base.make_request(url = "chats/messages", payload = query_string, type = "GET")
    
    def archive_chats(self, chatId: str):
        '''
        Archives the chat for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/archive', payload = payload, type = "POST")
    
    def unarchive_chats(self, chatId: str):
        '''
        Uarchives the chat for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/unarchive', payload = payload, type = "POST")
    
    def clear_messages(self, chatId: str):
        '''
        Clears all messages from the chat for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/clearMessages', payload = payload, type = "POST")
    
    def delete_chat(self, chatId: str):
        '''
        Deletes the chat from chat list for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/delete', payload = payload, type = "POST")

    def mark_chat_read(self, chatId: str):
        '''
        Marks chat message as read for the given chat ID.
        Uses POST request.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/read', payload = payload, type = "POST")
    

if __name__ == "__main__":
    try:
        load_dotenv("../.env")

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