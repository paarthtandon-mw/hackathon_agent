import asyncio
from gilbert.agent.agent import agent
from autogen_agentchat.ui import Console


asyncio.run(
    Console(agent.run_stream(task="Write a unique, Haiku about the weather in Paris"))
)
