import asyncio
from datetime import timedelta

from aiohttp import ClientSession
from arq import create_pool, cron, Worker
from arq.connections import RedisSettings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from periodic_tasks import check_not_sent_messages, check_no_answer_message, check_not_sent_to_telegram
import settings

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def startup(ctx):
    ctx["session"] = ClientSession()
    ctx["db_session"]: AsyncSession = async_session()


async def shutdown(ctx):
    await ctx["session"].close()
    await ctx['db_session'].close()


async def main():
    hours = set()
    for hour in range(6, 24):
        hours.add(hour)
    minutes = {10, 40}
    telegram_minutes = {20, 50}   # {2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57}
    fetch_minutes = {13, 23, 33, 43, 53}
    redis_pool = await create_pool(RedisSettings())
    worker = Worker(
        # указываем фоновые задачи
        cron_jobs=[
            cron(
                f"periodic_tasks.stable.{check_not_sent_messages.__name__}",
                hour=hours,
                minute=minutes
            ),
            cron(
                f"periodic_tasks.stable.{check_no_answer_message.__name__}",
                hour=hours,
                minute=fetch_minutes
            ),
            cron(
                f"periodic_tasks.telegram.{check_not_sent_to_telegram.__name__}",
                hour=hours,
                minute=telegram_minutes
            ),
        ],
        on_startup=startup,
        on_shutdown=shutdown,
        max_jobs=100,
        health_check_interval=60,
        handle_signals=False,
        redis_pool=redis_pool,
    )
    try:
        # запускаем воркер
        await worker.main()
    finally:
        # закрываем воркер
        await worker.close()
    # redis = await create_pool(RedisSettings())
    # await redis.enqueue_job(
    #     check_not_sent_messages.__name__,
    #     _defer_by=timedelta(minutes=1),
    # )


class WorkerSettings:
    hours = set()
    for hour in range(6, 24):
        hours.add(hour)
    functions = [check_not_sent_messages]
    cron_jobs = [
        cron(
            f"periodic_tasks.stable.{check_not_sent_messages.__name__}",
            hour=hours,
            minute=20
        )
    ]
    on_startup = startup
    on_shutdown = shutdown


if __name__ == "__main__":
    asyncio.run(main())
