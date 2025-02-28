import os
import sys
import json
from dotenv import load_dotenv

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils_ultraMsg.ultramsg_base import UltraMsgBase

class UltraMsgMessages:
    """
    Child class inherits UltraMsgBase class and implements methods to deal with messages in WhatsApp using the API.
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
        return self.umsg_base.make_request(url= 'messages/chat', type='POST', payload=payload)
    
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
        return self.umsg_base.make_request(url= 'messages/image', type='POST', payload=payload)

    def send_sticker(self, phone_number: int, sticker_url: str):
        '''
        Send a whatsapp sticker to the provided phone number.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param sticker_url: The http(s) url of the sticker. Note: It won't accept images from local disk.
        :type sticker_url: str

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&sticker={sticker_url}'
        return self.umsg_base.make_request(url= 'messages/sticker', type='POST', payload=payload)
    
    def send_document(self, phone_number: int, doc_name: str, doc_url: str, doc_caption: str):
        '''
        Send a document to the provided phone number along with a caption.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param doc_name: The name of the file.
        :type doc_name: str
        :param doc_url: The http(s) url of the document. Note: It won't accept documents from local disk.
        :type doc_url: str
        :param doc_caption: The text under the file.
        :type doc_caption: str

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&filename={doc_name}&document={doc_url}&caption={doc_caption}'
        return self.umsg_base.make_request(url= 'messages/document', type='POST', payload=payload)
    
    def send_audio(self, phone_number: int, audio_url: str):
        '''
        Send a audio clip to the provide phone number.
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param audio_url: The http(s) url of the audio. Note: It won't accept audio files from local disk.
        :type audio_url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&audio={audio_url}'
        return self.umsg_base.make_request(url = 'messages/audio', type = "POST", payload = payload)
    
    def send_voicenote(self, phone_number: int, voice_url: str):
        '''
        Sends a voice note to the provided phone number.\n
        Uses POST request.
        
        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param voice_url: The http(s) url of the voice note. Note: It won't accept voice notes from local disk.
        :type voice_url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&audio={voice_url}'
        return self.umsg_base.make_request(url = 'messages/voice', type = "POST", payload = payload)

    def send_video(self, phone_number: int, video_url: str, video_caption: str):
        '''
        Send a video on the provided number along with caption.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param video_url: The http(s) url of the video. Note It wont accept video files from local disk.
        :type video_url: str
        :param video_caption: The caption for the video.
        :type video_caption: str

        :returns: The response from the ultramsg server.
        rtype: str(json)
        '''
        payload = f'to={phone_number}&video={video_url}&caption={video_caption}'
        return self.umsg_base.make_request(url= 'messages/video', type='POST', payload=payload)

    def send_contact(self, phone_number: int, contact_id: str):
        '''
        Sends a contact ID to the provided phone number.\n
        Uses POST request.
        
        :param phone_number: The phone number of receipient along with country code,  without any space or extra characters such as (, ), -, +:
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
        return self.umsg_base.make_request(url = 'messages/contact', type = "POST", payload = payload)

    def send_location(self, phone_number: int, address: str, latitude: float, longitude: float):
        '''
        Send location to the provided phone number.\n
        Uses POST request.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param address: Text under the location. Supports two lines. To use two lines, use the \\n symbol.
        :type address: str
        :param latitude: Latitude of the address
        :type latitude: float
        :param longitude: Longitude of the address
        :type longitude: float

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&address={address}&lat={latitude}&lng={longitude}'
        return self.umsg_base.make_request(url = "messages/location", type = "POST", payload = payload)

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
        return self.umsg_base.make_request(url = "messages/vcard", type = "POST", payload = payload)
        
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
        return self.umsg_base.make_request(url = "messages/reaction", type = "POST", payload = payload)

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
        return self.umsg_base.make_request(url = "messages/delete", payload = payload, type = "POST")
    
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
        return self.umsg_base.make_request(url = "messages/resendByStatus", payload = payload, type = "POST")

    # Unable to get message ID.
    def resend_message_by_id(self, id: int):
        '''
        Resend a WhatsApp message given the ID of the message.\n
        Uses POST request.

        :param msgId: Status of the message to be deleted.
        :type msgId: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"id={id}"
        return self.umsg_base.make_request(url = "resendById", payload = payload, type = "POST")
        
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
        return self.umsg_base.make_request(url = "messages/clear", type = "POST", payload = payload)

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
        return self.umsg_base.make_request(url = 'messages', payload = query_string, type = "GET")

    def message_statistics(self):
        '''
        Get statistics of instance messages.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        return self.umsg_base.make_request(url = "messages/statistics", payload = None, type = "GET")

if __name__ == '__main__':
    # load_dotenv('utils/.env')
    load_dotenv('../.env')

    # from dotenv import load_dotenv # TODO: Remove this in production
    try:
        import sys  
        import os  
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        # print(f'Instance ID: {INSTANCE_ID}')
        # print(f'Token: {TOKEN}')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgMessages(um_base)

        print(um_msgs.delete_message_from_instance("all"))
        """
        print(f"Send message: {um_msgs.send_message('919674573242', 'Hello World, this is a test message from ultramsg python library.')}")

        print(f"Send image: {um_msgs.send_image('919674573242', 'https://images.pexels.com/photos/8007094/pexels-photo-8007094.jpeg', 'A man cycling.')}")

        print(f"Send sticker: {um_msgs.send_sticker('919674573242', 'https://www.gstatic.com/webp/gallery/3.jpg')}")

        print(f"Send document: {um_msgs.send_document('919674573242', 'CV', 'https://file-example.s3-accelerate.amazonaws.com/documents/cv.pdf', 'Resume')}")

        print(f"Send audio: {um_msgs.send_audio('919674573242', 'https://file-example.s3-accelerate.amazonaws.com/audio/2.mp3')}")

        print(f"Send voice note: {um_msgs.send_voicenote('919674573242', 'https://file-example.s3-accelerate.amazonaws.com/voice/oog_example.ogg')}")
        
        print(f"Send video: {um_msgs.send_video('919674573242', 'https://file-example.s3-accelerate.amazonaws.com/video/test.mp4', 'This is a sample video.')}")

        print(f"Send contact{um_msgs.send_contact('919674573242', '911234567890@c.us')}")

        send_loc_resp = um_msgs.send_location('919674573242', 'Office building \nBangalore', 12.918, 77.564)
        print("Send location: {0}".format(send_loc_resp))

        # Parse the response to a JSON object to get values
        json_resp = json.loads(send_loc_resp)
        send_loc_resp_id = json_resp['id']

        # Getting the following error: Resend message by id: {"error":"Path not found in Method: POST"}
        print(f'Resend message by id: {um_msgs.resend_message_by_id(send_loc_resp_id)}')

        print(f'Get statistics: {um_msgs.message_statistics()}')
        # # Data fields for the vcard method
        # name = 'Oliver;James'
        # full_name = 'James Oliver'
        # nickname = 'James'
        # birthdate = '1987-01-01'
        # gender = 'M'
        # note = 'Sample Note'

        """
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

        # vcard_resp = um_msgs.send_vcard('919674573242', vcard_data)
        # print(vcard_resp)


        # get_msg_resp = um_msgs.message_list(page = 1, limit = 1, status = "sent", sort = "desc")
        # json_resp = json.loads(get_msg_resp)
        # # print(json_resp)
        # msg_id = json_resp["messages"][0]
        # print(msg_id)
        # reaction_resp = um_msgs.react_to_message(msg_id, "👍")
        # print(reaction_resp)

        # print(um_msgs.resend_message_by_id(msg_id))

        # um_msgs.delete_message()   

        # # NOTE: Reaction not working even on Ultramsg
        # react_resp = um_msgs.react_to_message('true_919674573242@c.us_3EB09D4D6989D6BDC6E85C', '👍')     
        # print(react_resp)

        # # NOTE: Delete message not working from Ultramsg
        # del_resp = um_msgs.delete_message('true_919674573242@c.us_3EB09D4D6989D6BDC6E85C')
        # print(del_resp)
        
        print(um_msgs.message_list(1, 2, 'all', 'desc'))

    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")