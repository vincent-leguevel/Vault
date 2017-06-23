import os, json, encrypt

class Configuration:

    def __init__(self, source):
        if type(source) is str:
            self._set_source(source)
            self._set_configuration(json.load(self.source))
            self.file = True
        elif( type(source) is dict):
            self._set_source(source)
            self._set_conf(source)
            self.file = False
        else :
            raise ValueError("INVALID CONFIGURATION")

    def __str__(self):
        return json.dumps(self.conf)

    def _get_configuration(self):
        return self.conf

    def _set_configuration(self, conf):
        if type(conf) is not dict:
            raise ValueError("INVALID CONFIGURATION")
        self.conf = conf

    def _get_source(self):
        return self.source

    def _set_source(self, source):
        self.source = open(source, 'r+')

    def save(self):
        if(self.file):
            try:
                destination = open(self.source.name,'w')
                json.dump(self.conf, destination)
                destination.close()
            except Exception as e:
                raise e
            return True
        else:
            raise TypeError('TRYING TO SAVE A VOLATILE CONFIGURATION')

    def get(self, key):
        for indexKey in self.conf:
            if(indexKey == key):
                return self.conf[indexKey]
        raise KeyError("Invalid Key")

    def set(self, key, value):
        if not key in self.conf:
            raise KeyError("INVALID KEY")
        self.conf[key] = value

    conf = property(_get_configuration, _set_configuration)
    source = property(_get_source, _set_source)