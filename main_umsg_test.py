import os

# Remaining imports here
from dotenv import load_dotenv

from utils.ultramsg.base import UltraMsgBase
from utils.ultramsg.messages import UltraMsgMessages
from utils.ultramsg.chats import UltraMsgChats

load_dotenv('.env')

INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
TOKEN = os.getenv('UMSG_SECRET_KEY')

PHONE_NUMBER = '919674573242'

umsg_base = UltraMsgBase(instance_id = INSTANCE_ID, token = TOKEN)

um_msgs = UltraMsgMessages(umsg_base)
um_chats = UltraMsgChats(umsg_base)

print(um_msgs.send_message(PHONE_NUMBER, 'Final test of messages class.'))

# get_message_from_convo = um_msgs.delete_message("919674573242@c.us")
# print(get_message_from_convo)

print(um_chats.last_message(PHONE_NUMBER, 1))

# print(dir(UltraMsg))
