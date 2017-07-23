from configuration import Configuration
from user import User
import IHM, os

user_infos = Configuration('./configuration/user.conf.json')
user = User(user_infos.get('user').get('name'), user_infos.get('user').get('pass'), user_infos)

interface = IHM.interface('root',{'user': user})


os.system("pause")
