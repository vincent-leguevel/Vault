import os, json, encrypt

class Configuration:

    def __init__(self, source):
        if type(source) is str:
            self._source = open(source, 'r')
            self._conf = json.load(self._source)
            self._file = True
        elif( type(source) is dict):
            self._source = source
            self._conf = source
            self._file = False
        else :
            raise ValueError("INVALID CONFIGURATION")

    def __str__(self):
        return json.dumps(self._conf)

    def _get_configuration(self):
        return self._conf

    def _set_configuration(self, conf):
        if type(conf) is not dict:
            raise "INVALID CONFIGURATION"
        self._conf = conf

    def _get_source(self):
        return self._source

    def _set_source(self, source):
        self._source = open(source, 'r+')

    def save(self):
        if(self._file):
            try:
                destination = open(self._source.name,'w')
                json.dump(self._conf, destination)
                destination.close()
            except Exception as e:
                return False
            return True
        else:
            raise TypeError('TRYING TO SAVE A VOLATILE CONFIGURATION')

    def get(self, key):
        for indexKey in self._conf:
            if(indexKey == key):
                return self._conf[indexKey]
        raise "Invalid Key"

    def set(self, key, value):
        if not key in self._conf:
            raise "INVALID KEY"
        self._conf[key] = value

    conf = property(_get_configuration, _set_configuration)
    source = property(_get_source, _set_source)