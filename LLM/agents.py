# # LLM/agents.py

# from langchain.agents import initialize_agent, Tool
# from langchain_groq import ChatGroq
# from langchain.agents.agent_types import AgentType

# # Load the Groq LLM
# llm = ChatGroq(
#     model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
#     temperature=0
# )

# # Define a basic tool for testing
# def echo_tool(input_text: str) -> str:
#     return f"You said: {input_text}"

# tools = [
#     Tool(
#         name="EchoTool",
#         func=echo_tool,
#         description="Repeats what the user says for testing purposes."
#     )
# ]

# # Initialize the agent
# agent_executor = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# # Function to run the agent with a user prompt
# def run_agent(prompt: str) -> str:
#     return agent_executor.run(prompt)

# # agents.py

# class PDFExtractorAgent:
#     def __init__(self):
#         pass

#     def extract(self, file_path: str) -> str:
#         # Simple example using PyMuPDF
#         import fitz  # PyMuPDF
#         doc = fitz.open(file_path)
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         return text


# LLM/agents.py

# LLM/agents.py

from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
import fitz  # PyMuPDF

# =========================
# 🔹 LLM Initialization
# =========================
def load_llm():
    return ChatGroq(
        model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
        temperature=0
    )

# =========================
# 🔹 Tools
# =========================
def echo_tool(input_text: str) -> str:
    return f"You said: {input_text}"

def get_tools():
    return [
        Tool(
            name="EchoTool",
            func=echo_tool,
            description="Repeats what the user says for testing purposes."
        )
    ]

# =========================
# 🔹 Agent Executor
# =========================
def initialize_echo_agent():
    llm = load_llm()
    tools = get_tools()
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

def run_agent(prompt: str) -> str:
    agent_executor = initialize_echo_agent()
    return agent_executor.run(prompt)

# =========================
# 🔹 Custom Agent Classes
# =========================

class PDFExtractorAgent:
    def __init__(self):
        pass

    def extract(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

class TopicGeneratorAgent:
    def __init__(self):
        pass

    def generate(self, content: str) -> list:
        # Dummy logic for now
        return ["Topic 1", "Topic 2", "Topic 3"]

class SessionGeneratorAgent:
    def __init__(self):
        pass

    def generate_sessions(self, topic: str) -> list:
        # Dummy logic
        return [f"{topic} - Session 1", f"{topic} - Session 2"]

class EpisodeGeneratorAgent:
    def __init__(self):
        pass

    def generate_episodes(self, session: str) -> list:
        # Dummy logic
        return [f"{session} - Episode 1", f"{session} - Episode 2"]

class ScriptGeneratorAgent:
    def __init__(self):
        pass

    def generate_script(self, episode: str) -> str:
        # Dummy logic
        return f"Generated script for {episode}"
