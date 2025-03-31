import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from gilbert.agent.multi_agent_full_docs.prompts import (
    MAIN_SYSTEM_PROMPT,
    RETRIEVAL_SYSTEM_PROMPT,
)
from gilbert.tools.search import is_vaild_json, search


MAIN_AGENT_NAME = "media_intelligence_expert"
RETRIEVAL_AGENT_NAME = "retrieval_expert"

main_agent_tools = []
retrieval_agent_tools = [is_vaild_json, search]

openai_model = OpenAIChatCompletionClient(model="gpt-4o")
termination_condition = TextMentionTermination(
    text="FINAL MESSAGE:", sources=[MAIN_AGENT_NAME]
)


def load_all_txt_files(root_folder: str) -> str:
    all_text = ""
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".txt"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        all_text += file.read() + "\n"  # Add newline to separate files
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    return all_text


documentation = load_all_txt_files("gilbert/services/documentation_rag/docs")
RETRIEVAL_SYSTEM_PROMPT = f"{RETRIEVAL_SYSTEM_PROMPT}\n{documentation}"


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
