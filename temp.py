import os

from dotenv import load_dotenv

from utils.ultramsg.base import UltraMsgBase
from utils.ultramsg.messages import UltraMsgMessages

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
    