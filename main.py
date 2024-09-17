import uvicorn
from fastapi import FastAPI
import sentry_sdk

import settings
from aiogram import Bot
from routers import main_api_router

app = FastAPI(title="AI-stocker-bot")


sentry_sdk.init(
    dsn="https://77cc3f044de55ac08d59bfb2b4bd8ae4@o4507966814420992.ingest.de.sentry.io/4507968033259600",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
