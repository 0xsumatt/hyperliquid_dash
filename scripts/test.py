url = "https://api.hyperliquid.xyz/info"
headers = {"Content-Type": "application/json"}
import httpx


data = {
            "type": "clearinghouseState",
            "user": "0xdfc24b077bc1425ad1dea75bcb6f8158e10df303"
        }

req = httpx.post(url=url,headers=headers,json=data).json()
print(req)