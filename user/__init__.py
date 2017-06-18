import hashlib

class User:

    def __init__(self, conf):
        user = conf.get('user')
        self._name = user['name']
        self._password = user['pass']

    def _set_name(self, name):
        if type(name) is not str:
            raise "INVALID USERNAME"
        else:
            self._name = name

    def _get_name(self):
        return self._name

    def _set_password(self, password):
        if type(password) is not str:
            raise "INVALID PASSWORD"
        else:
            self._password = password

    def _get_password(self):
        raise "NOT AUTHORISED"

    #TODO redo avec crypto...
    def connect(self, username, user_password):
        password, salt = self.password.split(':')
        if not (self.name == username) and not(password == hashlib.sha256(salt.encode()+ user_password.encode).hexdigest()):
            return False
        return True

    name = property(_get_name, _set_name)
    password = property(_get_password, _set_password)
