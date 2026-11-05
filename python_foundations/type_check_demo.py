from typing import TypedDict


class Device(TypedDict):
    name: str
    online: bool


device: Device = {
    "name": "Router_A",
    "online": True
}

print(device)