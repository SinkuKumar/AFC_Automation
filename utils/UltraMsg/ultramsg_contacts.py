import os
from dotenv import load_dotenv
from ultramsg_base import UltraMsgBase

class UltraMsgContacts:
    """
    Child class inherits UltraMsgBase class and implements methods to deal with messages in WhatsApp using the API.\n
    Note
        Methods starting with `post_` use POST requests.
        Methods starting with `get_` use GET requests.
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def post_block(self, chatId: str):
        '''
        Block contact on WhatsApp for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = "contacts/block", payload = payload, type = "POST")
    
    def post_unblock(self, chatId: str):
        '''
        Unblock contact on WhatsApp for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&chatId={chatId}"
        return self.umsg_base.make_request(url = "contacts/unblock", payload = payload, type = "POST")
    
    def get_contacts(self):
        '''
        Get the contacts list.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "contacts", payload = query_string, type = "GET")
    
    def get_ids(self, clear: bool):
        '''
        Get the contact IDs.

        :param clear:
        :type clear: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "clear" : clear
        }
        return self.umsg_base.make_request(url = "contacts/ids", payload = query_string, type = "GET")
    
    def get_contact(self, chatId: str):
        '''
        Get the contact info for the given chat ID.

        :param chatId: chatId for contact or group.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chatId
        }
        return self.umsg_base.make_request(url = "contacts/contact", payload = query_string, type = "GET")
    
    def get_blocked(self):
        '''
        Get all blocked contacts.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "contacts/blocked", payload = query_string, type = "GET")
    
    def get_invalid(self, clear: bool):
        '''
        Get all invalid contacts.

        :param clear: 
        :type clear: bool
        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "clear" : clear
        }
        return self.umsg_base.make_request(url = "contacts/invalid", payload = query_string, type = "GET")
    
    def get_check_user(self, chatId: str, nocache: bool = False):
        '''
        Checks if user is WhatsApp user

        :param chatId: chatId for contact or group.
        :type chatId: str
        :param nocache: Whether to check the contacts cache or not.
            Contact information is normally cached for 3 days. By setting the nocache parameter to `True`, the cache will be bypassed ensuring a check is performed.
        :type nocache: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chatId,
            "nocache" : nocache
        }
        return self.umsg_base.make_request(url = "contacts/check", payload = query_string, type = "GET")
    
    def get_contact(self, chatId: str):
        '''
        Get the contact profile picture for the given chat ID.

        :param chatId: chatId for contact.
        :type chatId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "chatId" : chatId
        }
        return self.umsg_base.make_request(url = "contacts/image", payload = query_string, type = "GET")

if __name__ == '__main__':
    # from dotenv import load_dotenv # TODO: Remove this in production
    try:
        # TODO: Remove this later
        load_dotenv('../.env')

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgContacts(um_base)
    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")  