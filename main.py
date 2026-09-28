from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from datetime import datetime, timezone

import os
import httpx
from dotenv import load_dotenv


# اقرأ المتغيرات الموجودة داخل ملف .env
load_dotenv()


# أنشئ تطبيق FastAPI
app = FastAPI()


# شكل الـ event الذي نقبل استقباله
class Event(BaseModel):
    event_type: Literal[
        "page_visit",
        "book_click",
        "contact_click"
    ]
    page: Literal[
        "home",
        "booking",
        "contact",
    ] = "home"



# Route بسيط للتأكد أن السيرفر شغال
@app.get("/health")
def health():
    return {"status": "ok"}


# يأخذ Event ويحوّله إلى رسالة نصية
def telegram_message(event):

    # نختار النص حسب نوع الـ event
    if event.event_type == "book_click":
        event_text = "واحد يريد يحجز"

    elif event.event_type == "contact_click":
        event_text = "واحد يريد التواصل معك"

    else:
        event_text = "Page Visit"

    # وقت استلام الـ event بالـ UTC
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # نبني الرسالة النهائية
    message = (
        f"Event: {event_text}\n"
        f"Page: {event.page}\n"
        f"Time: {timestamp}"
    )

    # نرجع النص لمن استدعى هذه الدالة
    return message


# يأخذ الرسالة ويرسلها إلى Telegram
async def send_message_to_telegram(message):

    # اقرأ بيانات Telegram السرية من .env
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # عنوان Telegram API الخاص بإرسال الرسائل
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # البيانات التي Telegram يحتاجها
    telegram_data = {
        "chat_id": chat_id,
        "text": message,
    }

    # أرسل POST إلى Telegram وانتظر الرد
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=telegram_data
        )

    # مؤقتًا: نطبع رد Telegram لكي نعرف ماذا حصل
    print(response.status_code)
    print(response.text)


# استقبل event من /docs
@app.post("/event")
async def event(data: Event):

    # حول الـ event إلى نص
    message = telegram_message(data)

    # أرسل النص إلى Telegram
    await send_message_to_telegram(message)

    # أخبر الشخص الذي أرسل /event أن العملية انتهت
    return {"ok": True}
