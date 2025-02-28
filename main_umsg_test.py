
import os
import sys
# Remaining imports here
from dotenv import load_dotenv

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# After this do util imports here
# from utils import automation_exceptions

# from utils_ultraMsg.ultramsg_base import UltraMsgBase
# from utils_ultraMsg.ultramsg_messages import UltraMsgMessages
# from utils_ultraMsg.ultramsg_chats import UltraMsgChats
# from utils_ultraMsg.ultramsg_contacts import UltraMsgContacts
# from utils_ultraMsg.ultramsg_groups import UltraMsgGroups
# from utils_ultraMsg.ultramsg_instances import UltraMsgInstances
# from utils_ultraMsg.ultramsg_media import UltraMsgMedia

from utils_ultraMsg import UltraMsgBase, UltraMsgMessages, UltraMsgChats, UltraMsgContacts, UltraMsgGroups, UltraMsgInstances, UltraMsgMedia

load_dotenv('.env')

INSTANCE_ID = os.getenv('UMSG_INSTANCE_ID')
TOKEN = os.getenv('UMSG_SECRET_KEY')

umsg_base = UltraMsgBase(instance_id = INSTANCE_ID, token = TOKEN)

um_msgs = UltraMsgMessages(umsg_base)
um_chats = UltraMsgChats(umsg_base)

print(um_msgs.send_message('919674573242', 'Final test of messages class.'))

# get_message_from_convo = um_msgs.delete_message("919674573242@c.us")
# print(get_message_from_convo)

print(um_chats.last_message('919674573242@c.us', 1))

# print(dir(UltraMsg))