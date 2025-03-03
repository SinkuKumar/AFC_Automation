"""
Ultramsg Messages
-------------------

This module provides functionality to:
    1. Interact with messages.
    2. Send/delete messages.
    3. Get message statistics
with the help of Ultramsg WhatsApp API.

This module can be used as a standalone script, 
if that the `UMSG_INSTANCE_ID` and `UMSG_SECRET_KEY` environment variables are set.

:module: messages.py
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

class UltraMsgMessages:
    """
    Child class inherits UltraMsgBase class.
    Implements methods to deal with messages in WhatsApp using the API.\n
    """
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def send_message(self, phone_number: int, message: str):
        '''
        Send a whatsapp message to the provided phone number\n
        Uses POST request

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param message: The message to be sent to the receipient in UTF-16 encoding
        :type message: str

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&body={message}'
        return self.umsg_base.make_request(url= 'messages/chat',
                                           payload=payload, request_type='POST')

    def send_image(self, phone_number: int, image_url: str, image_caption: str):
        '''
        Send a image on the provided number along with caption.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param image_url: The http(s) url of the image. Note It wont accept images from local disk.
        :type image_url: str
        :param image_caption: The caption for the image.
        :type image_caption: str

        :returns: The response from the ultramsg server.
        rtype: str(json)
        '''
        payload = f'to={phone_number}&image={image_url}&caption={image_caption}'
        return self.umsg_base.make_request(url= 'messages/image',
                                           request_type='POST', payload=payload)

    def send_sticker(self, phone_number: int, sticker_url: str):
        '''
        Send a whatsapp sticker to the provided phone number.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param sticker_url: The http(s) url of the sticker. 
            Note: It won't accept images from local disk.
        :type sticker_url: str

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&sticker={sticker_url}'
        return self.umsg_base.make_request(url= 'messages/sticker',
                                           payload=payload, request_type='POST')

    def send_document(self, phone_number: int, doc_name: str, doc_url: str, doc_caption: str):
        '''
        Send a document to the provided phone number along with a caption.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param doc_name: The name of the file.
        :type doc_name: str
        :param doc_url: The http(s) url of the document. 
            Note: It won't accept documents from local disk.
        :type doc_url: str
        :param doc_caption: The text under the file.
        :type doc_caption: str

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&filename={doc_name}&document={doc_url}&caption={doc_caption}'
        return self.umsg_base.make_request(url= 'messages/document',
                                           payload=payload, request_type='POST')

    def send_audio(self, phone_number: int, audio_url: str):
        '''
        Send a audio clip to the provide phone number.
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param audio_url: The http(s) url of the audio. 
            Note: It won't accept audio files from local disk.
        :type audio_url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&audio={audio_url}'
        return self.umsg_base.make_request(url='messages/audio',
                                           payload=payload, request_type="POST")

    def send_voicenote(self, phone_number: int, voice_url: str):
        '''
        Sends a voice note to the provided phone number.\n
        Uses POST request.
        
        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param voice_url: The http(s) url of the voice note. 
        Note: It won't accept voice notes from local disk.
        :type voice_url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&audio={voice_url}'
        return self.umsg_base.make_request(url = 'messages/voice',
                                           payload = payload, request_type="POST")

    def send_video(self, phone_number: int, video_url: str, video_caption: str):
        '''
        Send a video on the provided number along with caption.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param video_url: The http(s) url of the video. 
            Note It wont accept video files from local disk.
        :type video_url: str
        :param video_caption: The caption for the video.
        :type video_caption: str

        :returns: The response from the ultramsg server.
        rtype: str(json)
        '''
        payload = f'to={phone_number}&video={video_url}&caption={video_caption}'
        return self.umsg_base.make_request(url= 'messages/video',
                                           payload=payload, request_type='POST')

    def send_contact(self, phone_number: int, contact_id: str):
        '''
        Sends a contact ID to the provided phone number.\n
        Uses POST request.
        
        :param phone_number: The phone number of receipient along with country code, 
            without any space or extra characters such as (, ), -, +:
            Eg: 911234567890
        :type phone_number: int
        :param contact_id: The contact ID or contact IDs. 
            The contact_id must be in the format: `<country_code><phone_number>@c.us`.<br>
            Eg: 14000000001@c.us or 14000000001@c.us,14000000002@c.us,14000000003@c.us
        :type contact_id: str or list(str)

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&contact={contact_id}'
        return self.umsg_base.make_request(url = 'messages/contact',
                                           payload = payload, request_type="POST")

    def send_location(self, phone_number: int, address: str, latitude: float, longitude: float):
        '''
        Send location to the provided phone number.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param address: Text under the location. 
            Supports two lines. To use two lines, use the \\n symbol.
        :type address: str
        :param latitude: Latitude of the address
        :type latitude: float
        :param longitude: Longitude of the address
        :type longitude: float

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&address={address}&lat={latitude}&lng={longitude}'
        return self.umsg_base.make_request(url = "messages/location",
                                           payload = payload, request_type="POST")

    def send_vcard(self, phone_number: int, text_card: str):
        '''
        Send a Virtual Contact File (VCF) to the given phone number.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param text_card: Text in the virtual contact card.
        :type text_card: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&vcard={text_card}'
        return self.umsg_base.make_request(url = "messages/vcard",
                                           payload = payload, request_type="POST")

    # Unable to get message ID.
    def react_to_message(self, message_id, emoji: str):
        '''
        Reacts to a message with a given message ID.\n
        Uses POST request.

        :param message_id: The message which should be reacted to.
        :type message_id: int
        :param emoji: Emoji to react with.
        :type emoji: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'msgId={message_id}&emoji={emoji}'
        return self.umsg_base.make_request(url = "messages/reaction",
                                           payload = payload, request_type="POST")

    # Unable to get message ID.
    def delete_message(self, msg_id: str):
        '''
        Deletes a WhatsApp message with the given message ID.\n
        Uses POST request.

        :param msgId: Message ID of the message to be deleted.
        :type msgId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'msgId={msg_id}'
        return self.umsg_base.make_request(url = "messages/delete",
                                           payload = payload, request_type="POST")

    def resend_message_by_status(self, status: str):
        '''
        Resends a WhatsApp message given the status of the message.\n
        Uses POST request.

        :param status: Status of the message to be deleted (unsent, expired).
        :type status: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"&status={status}"
        return self.umsg_base.make_request(url = "messages/resendByStatus",
                                           payload = payload, request_type="POST")

    # Unable to get message ID.
    def resend_message_by_id(self, req_id: int):
        '''
        Resend a WhatsApp message given the ID of the message.\n
        Uses POST request.

        :param msgId: Status of the message to be deleted.
        :type msgId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"id={req_id}"
        return self.umsg_base.make_request(url = "resendById",
                                           payload = payload, request_type="POST")

    def delete_message_from_instance(self, status: str):
        '''
        Clear the messages from an instance (queue, sent, unsent, invalid).\n
        Uses POST request.

        :param staus: Status of the message to be deleted (queue, sent, unsent, invalid)
        :type status: str
        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"status={status}"
        return self.umsg_base.make_request(url = "messages/clear",
                                           payload = payload, request_type="POST")

    def message_list(self, page: int, limit: int, status: str, sort: str):
        '''
        Get the list of instance messages (sent, queue, unsent, invalid all).
        Uses GET request.

        :param page: Pagination page number
        :type page: int
        :param limit: number of messages per request
        :type limit: int
        :param status: Status of the message (sent, queue, unsent, invalid, all)
        :type status: str
        :param sort: Order of sorting of messages (asc, desc)
        :type sort: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {
            "page" : page,
            "limit" : limit,
            "status" : status,
            "sort" : sort
        }
        return self.umsg_base.make_request(url = 'messages',
                                           payload = query_string, request_type = "GET")

    def message_statistics(self):
        '''
        Get statistics of instance messages.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        return self.umsg_base.make_request(url = "messages/statistics",
                                           payload = None, request_type = "GET")

if __name__ == '__main__':
    try:
        import os

        from dotenv import load_dotenv

        load_dotenv()

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgMessages(um_base)

        PHONE_NUMBER = '919674573242'

        print(f"Send message: {um_msgs.send_message(PHONE_NUMBER, 'Hello World, this is a test message from ultramsg python library.')}")
        print(f"Send image: {um_msgs.send_image(PHONE_NUMBER, 'https://images.pexels.com/photos/8007094/pexels-photo-8007094.jpeg', 'A man cycling.')}")
        print(f"Send sticker: {um_msgs.send_sticker(PHONE_NUMBER, 'https://www.gstatic.com/webp/gallery/3.jpg')}")
        print(f"Send document: {um_msgs.send_document(PHONE_NUMBER, 'CV', 'https://file-example.s3-accelerate.amazonaws.com/documents/cv.pdf', 'Resume')}")
        print(f"Send audio: {um_msgs.send_audio(PHONE_NUMBER, 'https://file-example.s3-accelerate.amazonaws.com/audio/2.mp3')}")
        print(f"Send voice note: {um_msgs.send_voicenote(PHONE_NUMBER, 'https://file-example.s3-accelerate.amazonaws.com/voice/oog_example.ogg')}")
        # print(f"Send message by ID: {um_msgs.delete_message(ID)}")
        # print(f'React to message: {um_msgs.react_to_message(ID)}')
        # print(f'Resend message by status: {um_msgs.resend_message_by_status("unsent")}')
        # print(f'Resend message by ID: {um_msgs.resend_message_by_id(ID)}')
        print(f'{um_msgs.delete_message_from_instance("sent")}')
        print(f'{um_msgs.message_list(1, 5, "sent", "asc")}')
        print(f'Message statistics: {um_msgs.message_statistics()}')

        # vcard_data = f"""BEGIN:VCARD
        # VERSION:3.0
        # N:{name}
        # FN:{full_name}
        # TEL;TYPE=CELL;waid=11234567890:+11234567890
        # NICKNAME:{nickname}
        # BDAY: {birthdate}
        # X-GENDER:{gender}
        # NOTE:{note}
        # ADR;TYPE=home:;;;;;;
        # ADR;TYPE=work:;;;;;;
        # END:VCARD"""
        # vcard_resp = um_msgs.send_vcard(phone_number, vcard_data)
        # print(f'Send virtual contact card: {um_msgs.send_vcard(phone_number, vcard_data)}')
    
    except Exception as e:
        print(f'Exception occurred: {e}')