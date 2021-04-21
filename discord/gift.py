from json import loads
import requests
from typing import Union, Optional
from datetime import datetime
from re import sub

class Gift:
    class GiftError(BaseException):
        def __init__(self, error = None) -> None:
            super().__init__(error)
        def __repr__(self):
            return "GiftError"
    
    class Time:
        def time(timeStr : str):
            try:
                return sub(r"[+-]([0-9]*):([0-9]*)$", "", str(datetime.strptime(timeStr or "2021-04-21T21:06:52+0000", "%Y-%m-%dT%H:%M:%S%z")))
            except:
                return None

    def __init__(self, code : str, token : str) -> None:
        self.code = code
        self.token = token
        self.gift = loads(requests.get(f"https://discord.com/api/v8/entitlements/gift-codes/{self.code}").content)
             
    def redeem(self) -> Union[dict, GiftError]:
        headers = {
            "Authorization": self.token,
            "payment_source_id": 'null'
        }
        res = loads(requests.post(f"https://discord.com/api/v8/entitlements/gift-codes/{self.code}/redeem", headers = headers).content)
        if res["code"] == 50050:
            raise self.GiftError(res["message"])
    
    def expires_at(self) -> Time.time:
        return self.Time.time(self.gift["expires_at"])

    def __repr__(self):
        return f"<Gift {self.code}>" 
    def __str__(self) -> str:
        return f"https://discord.gift/{self.code}"
