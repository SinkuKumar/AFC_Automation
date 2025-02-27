import os
from dotenv import load_dotenv
from .ultramsg_base import UltraMsgBase

class UltraMsgInstances:
    def __init__(self, ultramsg_base: UltraMsgBase):
        self.umsg_base = ultramsg_base

    def instance_status(self):
        '''
        Get the account status.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "instance/status", payload = query_string, type = "GET")

    def get_qr_image(self):
        '''
        Get QR image for authentication.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "instance/qr", type = "GET", payload = query_string)

    def get_qr_code(self):
        '''
        Get QR code for authentication.
        Uses GET code.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token1}"}
        return self.umsg_base.make_request(url = "instance/qrCode", payload = query_string)

    def phone_informations(self):
        '''
        Get connected phone informations.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "instance/me", payload = query_string)

    def get_instance_settings(self):
        '''
        Get settings for a particular instance.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json)        
        '''
        query_string = {"token" : f"{self.umsg_base.token}"}
        return self.umsg_base.make_request(url = "instance/settings", payload = query_string)

    def logout(self):
        '''
        Logout from WhatsApp Web to get new QR code.
        Uses GET request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json) 
        '''
        payload = f"token={self.umsg_base.token}"
        return self.umsg_base.make_request(url = "instance/logout", payload = payload)

    def restart(self):
        '''
        Restart our WhatsApp instance.
        Uses POST request.

        :returns: The json response from the ultramsg server.
        :rtype: str(json) 
        '''
        payload = f"token={self.umsg_base.token}"
        return self.umsg_base.make_request(url = "stance/restart", payload = payload)

    def settings(self, webhook_url: str, webhook_message_received: bool, webhook_message_create: bool, webhook_message_ack: bool, webhook_message_download_media, sendDelay: int = 1):
        '''
        Update WhatsApp instance settings.
        Uses POST request.

        :param webhook_url: HTTP or HTTPS URL for receiving notifications.
        :type webhook_url: str

        :param webhook_message_received: true/false notifications in webhooks when message received
        :type webhook_message_received: bool

        :param webhook_message_create: true/false notifications in webhooks when message create 
        :type param_webhook_create: bool

        :param webhook_message_ack: true/false ack (message delivered and message viewed) notifications in webhooks
        :type webhook_message_ack: bool

        :param webhook_message_download_media:

        :param sendDelay: Delay in seconds in sending message, defaults to 1.
        :type sendDelay: int

        :returns: The json response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}&sendDelay={sendDelay}&webhook_url={webhook_url}&webhook_message_received={webhook_message_received}&webhook_message_create={webhook_message_create}&webhook_message_ack={webhook_message_ack}&webhook_message_download_media={webhook_message_download_media}"
        return self.umsg_base.make_request(url = "instance/settings", payload = payload)

    def reset_to_default(self):
        '''
        Reset instance to default settings.
        Uses POST request.

        :returns: The response from the ultramsg server.
        :rtype: str(json)
        '''
        payload = f"token={self.umsg_base.token}"
        return self.umsg_base.make_request(url = "instance/clear", payload = payload)

"""
if __name__ == '__main__':
    try:
        load_dotenv('../.env')
        INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
        TOKEN = os.getenv('UMSG_SECRET_KEY')

        um_base = UltraMsgBase(instance_id=INSTANCE_ID, token=TOKEN)
        um_insts = UltraMsgInstances(um_base)

        get_inst_status_resp = um_insts.instance_status()
        print(f'Instance status: {get_inst_status_resp}')

        # get_qr_image_status = um_insts.get_qr_image()
        # print(type(get_qr_image_status))
        # print(get_qr_image_status)

        get_inst_settings_resp = um_insts.get_instance_settings()
        print(f'Instance settings{get_inst_settings_resp}')
    
    except Exception as e:
        print(f"Exception occurred: {(type(e).__name__)}: {e}")
"""