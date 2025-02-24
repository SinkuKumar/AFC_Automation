import os
import requests
import json
from dotenv import load_dotenv

class UltraMsgBase:
    def __init__(self, instance_id, token):
        'Initialize the ultramsg instance to further it to do commiunication with whatsapp'
        self.instance_id = instance_id
        self.token = token
        self.url = f'https://api.ultramsg.com/{self.instance_id}'
    
    def make_request(self, url, payload: str, type: str = 'POST'):
        '''
        Makes a request to ultramsg server with provided payload and required headers.

        ;param type: Type of the request to be made on ultramsg server, GET, POST. Defaults to POST.
        :type type: str
        :param payload: The payload(remaining part of the link apart from base url) to make a request to the server.
        :type payload: str

        returns: The response from the ultramsg server.
        rtype: str(json)
        '''
        self.req_url = f'{self.url}/{url}'
        self.payload = f'token={self.token}&{payload}'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request('POST', self.req_url, data=self.payload, headers=self.headers)
        return response.text

class UltraMsgMessages:
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def send_message(self, phone_number: int, message: str):
        '''
        Send a whatsapp message to the provided phone number

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
        Send a image on the provided number along with caption.

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
        Send a whatsapp sticker to the provided phone number

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
        Send a document to the provided phone number along with a caption.

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
        Sends a voice note to the provided phone number.
        
        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :para voice_url: The http(s) url of the voice note. Note: It won't accept voice notes from local disk.
        :type voice_url: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&audio={voice_url}'
        return self.umsg_base.make_request(url = 'messages/voice', type = "POST", payload = payload)

    def send_video(self, phone_number: int, video_url: str, video_caption: str):
        '''
        Send a video on the provided number along with caption.

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
        Sends a contact ID to the provided phone number.
        
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
        Send location to the provided phone number.

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
        Send a Virtual Contact File (VCF) to the given phone number.

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
        
    # Implement reaction method later, having some problems
    def send_reaction(self, message_id, emoji: str):
        '''
        Reacts to a message with a given message ID.

        :param message_id: The message which should be reacted to.
        :type message_id: int
        :param emoji: Emoji to react with.
        :type emoji: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'msgId={message_id}&emoji={emoji}'
        return self.umsg_base.make_request(url = "messages/reaction", type = "POST", payload = payload)

    def delete_message(self, message_id: str):
        '''
        Deletes a WhatsApp message with the given message_id.

        :param message_id: Message ID of the message to be deleted.
        :type message_id: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        pass
    
    def resend_by_status(self, status: str):
        '''
        Deletes a WhatsApp message given the status of the message.

        :param status: Status of the message to be deleted.
        :type status: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        pass

    def resend_by_id(self, id: str):
        '''
        Resend a WhatsApp message given the ID of the message.

        :param id: Status of the message to be deleted.
        :type id: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        pass

    def clear_message(self, status):
        '''
        Clear the messages from an instance (queue, sent or unsent)

        :param staus: Status of the message to be deleted (queue, sent, unsent, invalid)
        :type id: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        pass

    def get_messages(self, page: int, limit: int, status: str, sort: str):
        '''
        Get the list of instance messages (sent, queue, unsent, all)

        :param page: Pagination page number
        :type id: int
        :param limit: number of messages per request
        :type limit: int
        :param status: Status of the message (sent , queue , unsent , invalid)
        :type status: str
        :param sort: Order of sorting of messages (asc, desc)
        :type sort: str

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        pass

    def get_statistics(self):
        '''
        Get statistics of instance messages.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        pass

if __name__ == '__main__':
    # from dotenv import load_dotenv # TODO: Remove this in production
    try:
        # TODO: Remove this later
        load_dotenv('.env')

        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_msgs = UltraMsgMessages(um_base)

        # msg_resp = um_msgs.send_message('919674573242', 'Hello World, this is a test from ultramsg python library.')
        # print(msg_resp)

        # img_resp = um_msgs.send_image('919674573242', 'https://images.pexels.com/photos/8007094/pexels-photo-8007094.jpeg', 'A man cycling.')
        # print(img_resp)

        # sticker_resp = um_msgs.send_sticker('919674573242', 'https://www.gstatic.com/webp/gallery/3.jpg')
        # print(sticker_resp)

        # doc_resp = um_msgs.send_document('919674573242', 'CV', 'https://file-example.s3-accelerate.amazonaws.com/documents/cv.pdf', 'PFA my resume attached above.')
        # print(doc_resp)

        # audio_resp = um_msgs.send_audio("919674573242", "https://file-example.s3-accelerate.amazonaws.com/audio/2.mp3")
        # print(audio_resp)

        # audio_resp = um_msgs.send_audio("919674573242", "https://file-example.s3-accelerate.amazonaws.com/voice/oog_example.ogg")
        # print(audio_resp)
        
        # video_resp = um_msgs.send_video('919674573242', 'https://file-example.s3-accelerate.amazonaws.com/video/test.mp4', 'This is a sample video.')
        # print(video_resp)

        # contact_resp = um_msgs.send_contact("919674573242", "911234567890@c.us")
        # print(contact_resp)

        # location_resp = um_msgs.send_location('919674573242', 'Floor 2 Aasvhi Building, \n Veerendra Street, 100ft Ring Road, Banashankari', 12.918, 77.564)
        # print(location_resp)

        # Data fields for the vcard method
        # name = "Oliver;James"
        # full_name = "James Oliver"
        # nickname = "James"
        # birthdate = "1987-01-01"
        # gender = "M"
        # note = "Sample Note"

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



        # msg_resp = um_msgs.send_message('919674573242', 'Hello World, this message has to be reacted to.')
        # json_resp = json.loads(msg_resp)
        # print(json_resp)
        # msg_id = json_resp["id"]
        # print(msg_id)
        # reaction_resp = um_msgs.send_reaction(msg_id, "👍")
        # print(reaction_resp)


    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")