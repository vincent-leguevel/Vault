from configuration import Configuration
from user import User
import encrypt

user_infos = Configuration('./configuration/user.conf.json')
user = User(user_infos.get('user').get('name'), user_infos.get('user').get('pass'))

print user