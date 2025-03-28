from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from gilbert.agent.multi_agent.prompts import (
    MAIN_SYSTEM_PROMPT,
    RETRIEVAL_SYSTEM_PROMPT,
)
from gilbert.tools.search import ask_the_docs, is_vaild_json, search


MAIN_AGENT_NAME = "media_intelligence_expert"
RETRIEVAL_AGENT_NAME = "retrieval_expert"

main_agent_tools = []
retrieval_agent_tools = [ask_the_docs, is_vaild_json, search]

openai_model = OpenAIChatCompletionClient(model="gpt-4o")
termination_condition = TextMentionTermination(
    text="FINAL MESSAGE:", sources=[MAIN_AGENT_NAME]
)

main_agent = AssistantAgent(
    MAIN_AGENT_NAME,
    model_client=openai_model,
    tools=main_agent_tools,
    system_message=MAIN_SYSTEM_PROMPT,
    reflect_on_tool_use=True,
)
retrieval_agent = AssistantAgent(
    RETRIEVAL_AGENT_NAME,
    model_client=openai_model,
    tools=retrieval_agent_tools,
    system_message=RETRIEVAL_SYSTEM_PROMPT,
    reflect_on_tool_use=True,
)

team = RoundRobinGroupChat(
    [main_agent, retrieval_agent],
    termination_condition=termination_condition,
)
