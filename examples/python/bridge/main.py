from __future__ import annotations

from typing import Protocol

class Channel(Protocol):
    def send(self, text: str) -> str: ...

class EmailChannel:
    def send(self, text: str) -> str:
        return "email:" + text

class SmsChannel:
    def send(self, text: str) -> str:
        return "sms:" + text

class Notice:
    def __init__(self, channel: Channel) -> None:
        self._channel = channel
    def send(self, text: str) -> str:
        return self._channel.send(text)

class UrgentNotice(Notice):
    def send(self, text: str) -> str:
        return self._channel.send("!" + text)


if __name__ == "__main__":
    assert Notice(EmailChannel()).send("ready") == "email:ready"
    assert Notice(SmsChannel()).send("ready") == "sms:ready"
    assert UrgentNotice(EmailChannel()).send("ready") == "email:!ready"
    assert UrgentNotice(SmsChannel()).send("ready") == "sms:!ready"
    print("OK bridge")
