import os
from dotenv import load_dotenv
from ultramsg_base import UltraMsgBase

class UltraMsgChats:
    """
    Child class inherits UltraMsgBase class and implements methods to deal with messages in WhatsApp using the API.\n
    Note
        Methods starting with `post_` use POST requests.
        Methods starting with `get_` use GET requests.
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def get_chats(self):
        '''
        Get list of chats.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f'{self.umsg_base.token}'}
        return self.umsg_base.make_request(url = "chats", payload = query_string, type = "GET")
    
    def get_ids(self, clear: bool):
        '''
        Get the chat IDs.

        :param clear:
        :type clear: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "clear" : clear
        }
        return self.umsg_base.make_request(url = "chats/ids", payload = query_string, type = "GET")
    
    def get_messages(self, chatId: str, limit: int):
        '''
        Get last message from chat conversation for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :param limit: number of messages per request, max value: 1000
        :type limit: int

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chatId,
            "limit" : limit
        }
        return self.umsg_base.make_request(url = "chats/messages", payload = query_string, type = "GET")
    
    def post_archive_chats(self, chatId: str):
        '''
        Archives the chat for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/archive', payload = payload, type = "POST")
    
    def post_unarchive_chats(self, chatId: str):
        '''
        Uarchives the chat for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/unarchive', payload = payload, type = "POST")
    
    def post_clear_messages(self, chatId: str):
        '''
        Clears all messages from the chat for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/clearMessages', payload = payload, type = "POST")
    
    def post_delete_chat(self, chatId: str):
        '''
        Deletes the chat from chat list for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/delete', payload = payload, type = "POST")

    def post_chat_read(self, chatId: str):
        '''
        Marks chat message as read for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = 'chats/read', payload = payload, type = "POST")
    

if __name__ == "__main__":
    try:
        load_dotenv("../.env")

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgChats(um_base)

    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")