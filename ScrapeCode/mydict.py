class MyDict(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return 0