import os, random, struct, math
from Crypto.Cipher import AES


class encryptor:

    def __init__(self, conf):
        self._set_conf(conf)
        self.in_directory = os.path.realpath('./') + '/' + self.conf.get('file').get('in')
        self.out_directory = os.path.realpath('./') + '/' + self.conf.get('file').get('out')

    def symbol_generator(self):
        return {
            1: chr(int(math.ceil(25 * random.random()))+97),
            2: chr(int(math.ceil(25 * random.random()))+65),
            3: str(int(math.ceil(9 * random.random())))
        }[int(math.ceil(3 * random.random()))]

    def file_name_generator(self, length = 15):
        name = ''
        for i in range(length):
            name += self.symbol_generator()
        return name

    def encrypt_file(self, key, in_filename, out_filename = None, chunksize=64*1024):
        """ Encrypts a file using AES (CBC mode) with the
            given key.

            key:
                The encryption key - a string that must be
                either 16, 24 or 32 bytes long. Longer keys
                are more secure.

            in_filename:
                Name of the input file

            out_filename:
                If None, 'file_name_generator.enc' will be used.

            chunksize:
                Sets the size of the chunk which the function
                uses to read and encrypt the file. Larger chunk
                sizes can be faster for some files and machines.
                chunksize must be divisible by 16.
        """
        if not out_filename:
            out_filename = self.file_name_generator()

        in_file = self.in_directory + '/'  + in_filename

        out_file = self.out_directory + '/' + out_filename + '.enc'

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_file)

        with open(in_file, 'rb') as infile:
            with open(out_file, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(self, key, in_filename, out_filename=None, chunksize=24*1024):
        """ Decrypts a file using AES (CBC mode) with the
            given key. Parameters are similar to encrypt_file,
            with one difference: out_filename, if not supplied
            will be in_filename without its last extension
            (i.e. if in_filename is 'aaa.zip.enc' then
            out_filename will be 'aaa.zip')
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        out_file = self.in_directory + '/' + out_filename
        in_file = self.out_directory + '/' + in_filename

        with open(in_file, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_file, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)

    def del_encrypted_file(self, file_name):
        try:
            os.remove(self.out_directory + '/' + file_name)
        except Exception as e:
            raise e

    def save(self):
        self.conf.save()

    def _get_conf(self):
        return self.conf

    def _set_conf(self, conf):
        if not conf or (conf.__class__.__name__ is not 'Configuration' and type(conf) is not dict):
            raise ValueError("INVALID CONFIGURATION")
        self.conf = conf

    conf = property(_get_conf, _set_conf)
