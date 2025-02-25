import os
from dotenv import load_dotenv
from ultramsg_base import UltraMsgBase

class UltraMsgGroups:
    """
    Child class inherits UltraMsgBase class and implements methods to deal with messages in WhatsApp using the API.\n
    Note
        Methods starting with `post_` use POST requests.
        Methods starting with `get_` use GET requests.
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def get_groups(self):
        '''
        Get all groups info and participants.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "groups", payload = query_string, type = "GET")
    
    def get_group_ids(self, clear: bool):
        '''
        Get all group IDs.

        :param clear:
        :type clear: bool

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "clear" : clear
        }
        return self.umsg_base.make_request(url = "groups/ids", payload = query_string, type = "GET")

    def get_groups(self, groupId: str):
        '''
        Get group info and participants.

        :param groupId: ID of the group
        :type groupId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "token" : f"{self.umsg_base.token}",
            "groupId" : groupId
        }
        return self.umsg_base.make_request(url = "groups/group", payload = query_string, type = "GET")
    
if __name__ == '__main__':
    # from dotenv import load_dotenv # TODO: Remove this in production
    try:
        # TODO: Remove this later
        load_dotenv('../.env')

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgGroups(um_base)
    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")  