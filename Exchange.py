class myExchange:
    def __init__(self, name, key, privateKey, accessHandler):
        self.name = name
        self.key = key
        self.privateKey = privateKey
        self.accessHandler = accessHandler

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_key(self):
        return self.key

    def set_key(self, new_key):
        self.key = new_key

    def get_privateKey(self):
        return self.privateKey

    def set_privateKey(self, new_privateKey):
        self.privateKey = new_privateKey

    def get_accessHandler(self):
        return self.accessHandler

    def set_accessHandler(self, new_accessHandler):
        self.accessHandler = new_accessHandler


# Tx fee, transfer fee, maybe native coin fee implied as another colunn, fee depending on sizing in variations (1 btc sized is a different fee than a small? and lastly can you send margin and back in)
