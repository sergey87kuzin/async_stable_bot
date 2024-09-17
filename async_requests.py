import aiohttp


async def post(url: str, data: str = None, headers: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as response:
            if response and response.status == 200:
                return await response.json()
            return {"empty_answer": True}
