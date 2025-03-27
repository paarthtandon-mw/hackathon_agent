from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from gilbert.agent.prompts import SYSTEM_PROMPT


AGENT_NAME = "agent"

openai_model = OpenAIChatCompletionClient(model="gpt-4o")
termination_condition = TextMessageTermination(source=AGENT_NAME)
tools = []

chat_agent = AssistantAgent(
    AGENT_NAME,
    model_client=openai_model,
    tools=tools,
    system_message=SYSTEM_PROMPT,
    reflect_on_tool_use=True,
)

agent = RoundRobinGroupChat(
    [chat_agent],
    termination_condition=termination_condition,
)
