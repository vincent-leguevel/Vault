valid_type = ['AES']

class File:

    def __init__(self, source_name, encrypted_name, encrypt_type, encryption_key):
        if(not source_name or not encrypted_name or not encrypt_type or not encryption_key):
            raise ValueError('INVALID INFORMATION')

        self._set_source_name(source_name)
        self._set_encrypted_name(encrypted_name)
        self._set_encrypted_type(encrypt_type)
        self._set_encryption_key(encryption_key)

    def __str__(self):
        return str(self.get_file())

    def get_file(self):
        return {
            'name': str(self.source_name),
            'encrypted_name': str(self.encrypted_name),
            'key': str(self.encryption_key),
            'algo': str(self.encrypted_type)
        }

    def save(self):
        return self.get_file()

    def valid_entry(self, entry):
        if not entry or (type(entry) is not str and type(entry) is not unicode):
            raise ValueError('INVALID VALUE')
        else:
            return True

    def _set_source_name(self, entry):
        if(self.valid_entry(entry)):
            self.source_name = entry

    def _get_source_name(self):
        return self.source_name

    def _set_encrypted_name(self, entry):
        if(self.valid_entry(entry)):
            self.encrypted_name = entry

    def _get_encrypted_name(self):
        return self.encrypted_name

    def _set_encrypted_type(self, entry):
        if not entry in valid_type:
            raise ValueError('INVALID TYPE')
        if self.valid_entry(entry):
            self.encrypted_type = entry

    def _get_encrypted_type(self):
        return self.encrypted_type

    def _set_encryption_key(self, entry):
        if(self.valid_entry(entry)):
            self.encryption_key = entry

    def _get_encryption_key(self):
        return self.encryption_key

    source_name = property(_set_source_name, _get_source_name)
    encrypted_name = property(_set_encrypted_name, _get_encrypted_name)
    encrypted_type = property(_set_encrypted_type, _get_encrypted_type)
    encryption_key = property(_set_encryption_key, _get_encryption_key)



class FilesList:

    def __init__(self, file_conf, file_list = None):
        self.files = []
        if file_list is not None:
            if type(file_list) is not list:
                raise TypeError("FILE_LIST INVALID TYPE")

        if not file_conf or file_conf.__class__.__name__ is not 'Configuration':
            raise TypeError("INVALID TYPE")

        self.conf = file_conf

        if file_list:
            for file in file_list:
                self.add_file(file)

    def __str__(self):
        res = "[\n"
        for file in self.files:
            res += str(file)+",\n"
        res += "]"
        return res

    def add_file(self, file):
        if not file or (file.__class__.__name__ is not 'File' and type(file) is not dict):
            raise ValueError("INVALID FILE VALUE")
        if type(file) is dict:
            try:
                new_file = File(file['name'], file['encrypted_name'], file['algo'], file['key'])
            except Exception as e:
                raise e
            file = new_file
        self.files.append(file)

    def get_file(self, name):
        for file in self.files:
            if file.source_name == name:
                return file.get_file()

    def del_file(self, name):
        for file in self.files:
            if file.source_name == name:
                self.files.pop(self.files.index(file))

    def save(self):
        savable = [file.save() for file in self.files]
        self.conf.set('files', savable)
        self.conf.save()

    def _get_files(self):
        return self.files

    def _set_files(self, value):
        self.files = value

    files = property(_get_files, _set_files)