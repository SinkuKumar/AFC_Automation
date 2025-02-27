
import os
import sys
# Remaining imports here
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# After this do util imports here
from utils.UltraMsg.ultramsg_base import UltraMsgBase
from utils.UltraMsg.ultramsg_chats import UltraMsgChats
from utils.UltraMsg.ultramsg_messages import UltraMsgMessages

load_dotenv('utils/.env')

INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
TOKEN = os.getenv('UMSG_SECRET_KEY')

umsg_base = UltraMsgBase(instance_id = INSTANCE_ID, token = TOKEN)

um_msgs = UltraMsgMessages(umsg_base)
um_chats = UltraMsgChats(umsg_base)

print(um_msgs.send_message('919674573242', 'Final test of messages class.'))

# get_message_from_convo = um_msgs.delete_message("919674573242@c.us")
# print(get_message_from_convo)

# print(um_chats.last_message('919674573242@c.us', 1))

# print(dir(UltraMsg))