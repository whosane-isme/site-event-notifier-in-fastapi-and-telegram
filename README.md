# Site Event Notifier

A small FastAPI service that receives website events and sends notifications to Telegram.

## About this repository

This is a manually rewritten and organized version of my earlier vibe-coded project, [tbot](https://github.com/whosane-isme/tbot). I am rebuilding it step by step so I understand how each part works and can maintain it myself.

## What it does

- Accepts `page_visit`, `book_click`, and `contact_click` events at `POST /event`.
- Validates the request with Pydantic.
- Formats the event with a UTC timestamp and sends it to the Telegram chat configured in `.env`.
- Provides `GET /health` to check that the API is running.

This is an early learning project. Right now, every event goes to one Telegram chat configured by the project owner. It is not yet a hosted multi-user service.

## Run it locally

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with `.\.venv\Scripts\Activate.ps1`.

2. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`, then add your Telegram bot token and chat ID. Keep `.env` private; it is ignored by Git.

4. Start the API:

   ```bash
   python -m uvicorn main:app --reload
   ```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to send a test event, or [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) to check the server.

Example request for `POST /event`:

```json
{
  "event_type": "book_click",
  "page": "Hotel Demo"
}
```

## Next steps

The next improvements are to handle missing or invalid Telegram settings clearly, then learn how API keys and per-project settings could support more than one user. A client library and automatic uptime checks can wait until the core service is reliable.

## شغلات تافهة تعلمتها بالطريق

ها وصدگ، تعلمت أستخدم `make` همين، وسويت اختصارات حتى ما أظل كل مرة أكتب نفس أوامر الـvenv وUvicorn. أول مرة شغّل `make venv` حتى ينشئ البيئة ويثبت المكتبات، وبعدها كل مرة تريد تشغّل السيرفر استخدم `make uvicorn`.

وإذا واحد يريد يبني نفس الأداة بإيده خطوة خطوة، خليت الـAI يسويلي [دوكيومنت يشرح طريقة بنائها من البداية](https://github.com/whosane-isme/tbot/blob/main/REBUILD_MAIN_PY.md).
