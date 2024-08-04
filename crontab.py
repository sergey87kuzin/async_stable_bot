import asyncio
from datetime import timedelta

from aiohttp import ClientSession
from arq import create_pool, cron
from arq.connections import RedisSettings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from periodic_tasks.stable import check_not_sent_messages
import settings

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def startup(ctx):
    ctx["session"] = ClientSession()
    ctx["db_session"]: AsyncSession = async_session()


async def shutdown(ctx):
    await ctx['db_session'].close()


async def main():
    redis = await create_pool(RedisSettings())
    await redis.enqueue_job(
        check_not_sent_messages.__name__,
        _defer_by=timedelta(minutes=1),
    )


class WorkerSettings:
    hours = set()
    for hour in range(6, 24):
        hours.add(hour)
    functions = [check_not_sent_messages]
    cron_jobs = [
        cron(
            f"periodic_tasks.stable.{check_not_sent_messages.__name__}",
            hour=hours,
            minute=10
        )
    ]
    on_startup = startup
    on_shutdown = shutdown


if __name__ == "__main__":
    asyncio.run(main())