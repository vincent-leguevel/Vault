import hashlib, uuid

class User:

    def __init__(self, username, password, conf=None):
        if(not username or not password):
            raise ValueError('INVALID ENTRY: SHOULD HAVE name AND pass KEY')
        if type(password) is not str and type(password) is not unicode or type(username) is not str and type(username) is not unicode:
            raise ValueError('INVALID ENTRY')
        self._set_name(username)
        self.password = password
        if conf:
            self._conf = conf

    def __str__(self):
        return self.name

    def _set_name(self, name):
        if type(name) is not str and type(name) is not unicode:
            raise ValueError("INVALID USERNAME")
        else:
            self.name = name

    def _get_name(self):
        return self.name

    def _set_password(self, password):
        print 'set_password'
        if type(password) is not str and type(password) is not unicode:
            raise ValueError("INVALID PASSWORD")
        else:
            if len(password) < 6 :
                raise ValueError("INVALID PASSWORD: TO SHORT")
            salt = uuid.uuid4().hex
            self.password = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+':'+salt.encode()

    def _get_password(self):
        return self.password

    def verify_password(self, entry):
        password, salt = self.password.split(':')
        print password, salt, hashlib.sha256(salt.encode()+ entry.encode()).hexdigest()
        if password == hashlib.sha256(salt.encode()+ entry.encode()).hexdigest():
            return True
        return False

    def connect(self, username, user_password):
        if not (self.name == username) or not self.verify_password(user_password):
            return False
        return True

    def inscription(self, username, password, verify_password):
        if(not username or not password or not verify_password or password != verify_password):
            raise ValueError('INVALID INFORMATION')
        self._set_password(password)
        self.name = username
        return self.save()

    def save(self):
        if hasattr(self, '_conf'):
            self._conf.set('user',{
                "name": self.name,
                "pass": self.password
            })
            as_been_saved = self._conf.save()
            return as_been_saved
        raise TypeError("TRYING TO SAVE VOLATILE USER")

    name = property(_get_name, _set_name)
    password = property(_get_password, _set_password)
