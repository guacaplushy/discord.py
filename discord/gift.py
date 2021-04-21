from json import loads
import requests

class GiftError(BaseException):
    def __init__(self, error):
        super().__init__(error)
    def __repr__(self):
        return "GiftError"
    
class Gift:
    def __init__(self, code : str, token : str):
        self.code = code
        self.token = token
        gift = requests.get(f"https://discord.com/api/v8/entitlements/gift-codes/{self.code}")
        print(gift)
             
    def redeem(self) -> dict:
        headers = {
            "Authorization": self.token,
            "payment_source_id": 'null'
        }
        return loads(requests.post(f"https://discord.com/api/v8/entitlements/gift-codes/{self.code}/redeem", headers = headers).content)

    def __repr__(self):
        return f"<Gift code={self.code}>" 
