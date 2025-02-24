import os
import requests


class UltraMsgBase:
    def __init__(self, instance_id, token):
        'Initialize the ultramsg instance to further it to do commiunication with whatsapp'
        self.instance_id = instance_id
        self.token = token
        self.url = f'https://api.ultramsg.com/{self.instance_id}'
    
    def make_request(self, url, payload, type = 'POST'):
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

    def send_message(self, phone_number, message):
        '''
        Send a whatsapp message to the provided phone number

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 Without any space or extra characters such as (, ), -, +
        :type phone_number: int
        :param message: The message to be sent to the receipient in UTF-16 encoding
        :type message: str

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f'to={phone_number}&body={message}'
        return self.umsg_base.make_request(url= 'messages/chat', type='POST', payload=payload)
    
    def send_image(self, phone_number, image_url, image_caption):
        '''
        Send a image on the provided number along with caption.

        :param phone_number: The phone number of receipient along with country code: 
            Eg: 919717415826 Without any space or extra characters such as (, ), -, +
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




if __name__ == '__main__':
    from dotenv import load_dotenv # TODO: Remove this in production

    # TODO: Remove this later
    load_dotenv('./utils/.env')

    INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
    TOKEN = os.getenv('UMSG_SECRET_KEY')
    um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
    um_msgs = UltraMsgMessages(um_base)
    # msg_resp = um_msgs.send_message('919717425826', 'Hello World, this is a test from ultramsg python library.')
    # print(msg_resp)
    img_resp = um_msgs.send_image('919717425826', 'https://images.pexels.com/photos/8007094/pexels-photo-8007094.jpeg', 'A girl playing badminton.')
    print(img_resp)
