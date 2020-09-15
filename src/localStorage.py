class localStorage():
    _storage = {}
    @staticmethod
    def setItem(key, value):
        localStorage._storage[key] = value
    @staticmethod
    def getItem(key):
        return localStorage._storage[key]
    @staticmethod
    def removeItem(key):
        del localStorage._storage[key]
    @staticmethod
    def clear(key):
        localStorage._storage = {}