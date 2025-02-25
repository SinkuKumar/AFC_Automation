import os
from dotenv import load_dotenv
from ultramsg_base import UltraMsgBase

class UltraMsgMedia:
    """
    Child class inherits UltraMsgBase class and implements methods to deal with messages in WhatsApp using the API.\n
    Note
        Methods starting with `post_` use POST requests.
        Methods starting with `get_` use GET requests.
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def post_upload(self, file: str):
        '''
        Upload media from device.

        :param file: from URL or from your local device.
        :type file: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&file={file}"
        return self.umsg_base.make_request(url = "media/upload", payload = payload, type = "POST")
    
    def post_delete(self, url: str):
        '''
        Delete media from device.

        :param url: the URL of the media file.
        :type url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&url={url}"
        return self.umsg_base.make_request(url = "media/delete", payload = payload, type = "POST")
    
    def post_delete(self, date: str):
        '''
        Delete media from device.

        :param date: month and year
            Example :1-2023 or 01-2023
        :type date: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&url={date}"
        return self.umsg_base.make_request(url = "media/deleteByDate", payload = payload, type = "POST")
    
if __name__ == '__main__':
    # from dotenv import load_dotenv # TODO: Remove this in production
    try:
        # TODO: Remove this later
        load_dotenv('../.env')

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgMedia(um_base)
    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")  