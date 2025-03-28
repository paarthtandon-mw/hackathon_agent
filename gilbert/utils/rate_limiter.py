import asyncio
from aiolimiter import AsyncLimiter

# Max 100 requests per minute
rate_limiter = AsyncLimiter(max_rate=100, time_period=60)
concurrency_semaphore = asyncio.Semaphore(10)
