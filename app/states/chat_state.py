import reflex as rx
from typing import TypedDict
import datetime
import asyncio
import random


class Message(TypedDict):
    sender: str
    text: str
    timestamp: str
    avatar: str


class ChatState(rx.State):
    messages: list[Message] = []
    is_typing: bool = False

    @rx.event
    def send_message(self, form_data: dict):
        message_text = form_data.get("message", "").strip()
        if not message_text:
            return
        user_avatar = "https://api.dicebear.com/9.x/initials/svg?seed=User"
        self.messages.append(
            {
                "sender": "You",
                "text": message_text,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "avatar": user_avatar,
            }
        )
        yield
        return ChatState.persona_reply

    @rx.event(background=True)
    async def persona_reply(self):
        async with self:
            self.is_typing = True
        await asyncio.sleep(random.uniform(1, 2.5))
        async with self:
            user_name = "Alex"
            persona_avatar = (
                f"https://api.dicebear.com/9.x/initials/svg?seed={user_name}"
            )
            self.messages.append(
                {
                    "sender": user_name,
                    "text": "That's an interesting point! I'll look into it.",
                    "timestamp": datetime.datetime.now().strftime("%H:%M"),
                    "avatar": persona_avatar,
                }
            )
            self.is_typing = False