from typing import List, cast

import chainlit as cl
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat

from gilbert.agent.multi_agent.the_bois import team


@cl.on_chat_start
async def start_chat() -> None:
    cl.user_session.set("prompt_history", "")
    cl.user_session.set("team", team)


@cl.set_starters
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Poem Writing",
            message="Write a poem about the ocean.",
        ),
        cl.Starter(
            label="Story Writing",
            message="Write a story about a detective solving a mystery.",
        ),
        cl.Starter(
            label="Write Code",
            message="Write a function that merge two list of numbers into single sorted list.",
        ),
    ]


@cl.on_message
async def chat(message: cl.Message) -> None:
    team = cast(RoundRobinGroupChat, cl.user_session.get("team"))
    streaming_response: cl.Message | None = None

    async for msg in team.run_stream(task=message.content):
        if isinstance(msg, ModelClientStreamingChunkEvent):
            if streaming_response is None:
                streaming_response = cl.Message(
                    content=f"{msg.source}: ", author=msg.source
                )
            await streaming_response.stream_token(msg.content)

        elif isinstance(msg, TextMessage):
            # Finish any ongoing stream
            if streaming_response is not None:
                await streaming_response.send()
                streaming_response = None

            await cl.Message(content=msg.content, author=msg.source).send()

        elif isinstance(msg, TaskResult):
            if streaming_response is not None:
                await streaming_response.send()
                streaming_response = None

            final_message = "Task terminated."
            if msg.stop_reason:
                final_message += f" Reason: {msg.stop_reason}"
            await cl.Message(content=final_message).send()

        else:
            # Add a debug logger here if you're unsure what's being skipped
            print(
                f"Skipped message type: {type(msg)} — {getattr(msg, 'content', None)}"
            )
