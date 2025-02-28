import requests

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
        response = requests.request(type, self.req_url, data=self.payload, headers=self.headers)
        # print(response)  # remove this after testing
        return response.text