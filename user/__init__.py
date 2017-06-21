import hashlib, uuid

class User:

    def __init__(self, username, password, conf):
        if(not username or not password):
            raise ValueError('INVALID ENTRY: SHOULD HAVE name AND pass KEY')
        if type(password) is not str and type(password) is not unicode or type(username) is not str and type(username) is not unicode:
            raise ValueError('INVALID ENTRY')
        self._name = username
        self._password = password
        self._conf = conf

    def __str__(self):
        return self._name

    def _set_name(self, name):
        if type(name) is not str and type(name) is not unicode:
            raise ValueError("INVALID USERNAME")
        else:
            self._name = name

    def _get_name(self):
        return self._name

    def _set_password(self, password):
        if type(password) is not str and type(password) is not unicode:
            raise ValueError("INVALID PASSWORD")
        else:
            if len(password) < 6 :
                raise ValueError("INVALID PASSWORD: TO SHORT")
            salt = uuid.uuid4().hex
            self._password = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+':'+salt.encode()

    def _get_password(self):
        raise KeyError("NOT AUTHORISED")

    def verify_password(self, entry):
        password, salt = self._password.split(':')
        if password == hashlib.sha256(salt.encode()+ entry.encode()).hexdigest():
            return True
        return False

    def connect(self, username, user_password):
        if not (self._name == username) and not self.verify_password(user_password):
            return False
        return True

    def inscription(self, username, password, verify_password):
        if(not username or not password or not verify_password or password != verify_password):
            raise ValueError('INVALID INFORMATION')
        self._set_password(password)
        self._set_name(username)
        return self.save()

    def save(self):
        self._conf.set('user',{
            "name": self._get_name(),
            "pass": self._password
        })
        try:
            as_been_saved = self._conf.save()
        except Exception as e:
            if e is TypeError:
                raise TypeError("TRYING TO SAVE VOLATILE USER")
        return as_been_saved

    name = property(_get_name, _set_name)
    password = property(_get_password, _set_password)
