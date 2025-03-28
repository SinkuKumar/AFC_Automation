"""
Ultramsg Media
-------------------

This module provides functionality to interact with media files with the help of Ultramsg WhatsApp API.

This module can be used as a standalone script, if the `UMSG_INSTANCE_ID` and `UMSG_SECRET_KEY` environment variables are set.

:module: media.py
:platform: Unix, Windows

:date: March 3, 2025
:author: Niladri Mallik <niladrimallik.p@hq.graphxsys.com>

# TODO: Implement logging
# TODO: Add error handling
# TODO: Implement error codes
"""

import os
import sys

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.ultramsg.base import UltraMsgBase

class UltraMsgMedia:
    """
    Child class inherits UltraMsgBase class.
    Implements methods to deal with media files in WhatsApp using the API.\n
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def upload_media(self, file: str):
        '''
        Upload media from device.
        Uses POST request.

        :param file: from URL or from your local device.
        :type file: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"file={file}"
        return self.umsg_base.make_request(url="media/upload",
                                           payload=payload, request_type="POST")

    def delete_media(self, url: str):
        '''
        Delete media from device.
        Uses POST request.

        :param url: the URL of the media file.
        :type url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"url={url}"
        return self.umsg_base.make_request(url="media/delete",
                                           payload=payload, request_type="POST")

    def delete_media_by_date(self, date: str):
        '''
        Delete media from device by date.
        Uses POST request.

        :param date: month and year
            Example :1-2023 or 01-2023
        :type date: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"url={date}"
        return self.umsg_base.make_request(url="media/deleteByDate",
                                           payload=payload, request_type="POST")

if __name__ == '__main__':
    try:
        import os

        from dotenv import load_dotenv

        # TODO: Remove this later in production
        load_dotenv('../.env')

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgMedia(um_base)
    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")  
