import json

class Config:
    def __init__(self, path):
        self.path = path
        self.config = None
    
    def loadConfig(self):
        self.config = json.load(open(self.path))    

