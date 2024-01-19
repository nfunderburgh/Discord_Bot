from typing import TypedDict


class Prayer(TypedDict):
    prayerId: int
    name: str
    anonymous: bool
    prayerRequest: str
