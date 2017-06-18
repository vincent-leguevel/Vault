from configuration import Configuration
from user import User

conf = Configuration('./configuration/conf.json')

test = User(conf)

print(test.connect(1, 'test'))

