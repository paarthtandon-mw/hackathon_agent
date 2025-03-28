import asyncio
import json
import traceback
import os

from gilbert.services.ir.client import async_ir_client
from gilbert.utils.rate_limiter import rate_limiter, concurrency_semaphore


async def ask_the_docs(request: str) -> str:
    """Ask the documentation database a question, or give the database a command"""
    command = f'graphrag query --root ./gilbert/services/documentation_rag --method local --query "{request}"'
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {process.returncode}:\n{stderr.decode().strip()}"
        )

    return stdout.decode().strip()


async def is_vaild_json(json_query: str) -> str:
    """Tests if a given string is valid json"""
    try:
        json.loads(json_query)
    except Exception as _:
        return traceback.format_exc()
    return "valid"


async def search(search_request_json: str) -> dict:
    async with concurrency_semaphore:
        async with rate_limiter:
            payload = json.loads(search_request_json)

            company_id = os.environ["COMPANY_ID"]
            product_type = os.environ["PRODUCT_TYPE"]

            if not company_id or not product_type:
                raise EnvironmentError(
                    "Missing required environment variables: COMPANY_ID and/or PRODUCT_TYPE"
                )

            payload["modifiers"] = {
                "requestorCompanyId": company_id,
                "productType": product_type,
            }

            response = await async_ir_client().post(payload)
            return response
