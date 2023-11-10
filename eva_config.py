class Config:
    def __init__(self) -> None:
        self.open_ai_key = ""
        self.refuel_key = ""

    def get_open_ai_key(self):
        return self.open_ai_key
    
    def get_refuel_key(self):
        return self.refuel_key