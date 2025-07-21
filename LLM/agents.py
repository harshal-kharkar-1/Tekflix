# # # # LLM/agents.py

# # # from langchain.agents import initialize_agent, Tool
# # # from langchain_groq import ChatGroq
# # # from langchain.agents.agent_types import AgentType

# # # # Load the Groq LLM
# # # llm = ChatGroq(
# # #     model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
# # #     temperature=0
# # # )

# # # # Define a basic tool for testing
# # # def echo_tool(input_text: str) -> str:
# # #     return f"You said: {input_text}"

# # # tools = [
# # #     Tool(
# # #         name="EchoTool",
# # #         func=echo_tool,
# # #         description="Repeats what the user says for testing purposes."
# # #     )
# # # ]

# # # # Initialize the agent
# # # agent_executor = initialize_agent(
# # #     tools=tools,
# # #     llm=llm,
# # #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# # #     verbose=True
# # # )

# # # # Function to run the agent with a user prompt
# # # def run_agent(prompt: str) -> str:
# # #     return agent_executor.run(prompt)

# # # # agents.py

# # # class PDFExtractorAgent:
# # #     def __init__(self):
# # #         pass

# # #     def extract(self, file_path: str) -> str:
# # #         # Simple example using PyMuPDF
# # #         import fitz  # PyMuPDF
# # #         doc = fitz.open(file_path)
# # #         text = ""
# # #         for page in doc:
# # #             text += page.get_text()
# # #         return text


# # # LLM/agents.py

# # # LLM/agents.py

# # from langchain.agents import initialize_agent, Tool
# # from langchain_groq import ChatGroq
# # from langchain.agents.agent_types import AgentType
# # import fitz  # PyMuPDF

# # # =========================
# # # 🔹 LLM Initialization
# # # =========================
# # def load_llm():
# #     return ChatGroq(
# #         model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
# #         temperature=0
# #     )

# # # =========================
# # # 🔹 Tools
# # # =========================
# # def echo_tool(input_text: str) -> str:
# #     return f"You said: {input_text}"

# # def get_tools():
# #     return [
# #         Tool(
# #             name="EchoTool",
# #             func=echo_tool,
# #             description="Repeats what the user says for testing purposes."
# #         )
# #     ]

# # # =========================
# # # 🔹 Agent Executor
# # # =========================
# # def initialize_echo_agent():
# #     llm = load_llm()
# #     tools = get_tools()
# #     return initialize_agent(
# #         tools=tools,
# #         llm=llm,
# #         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# #         verbose=True
# #     )

# # def run_agent(prompt: str) -> str:
# #     agent_executor = initialize_echo_agent()
# #     return agent_executor.run(prompt)

# # # =========================
# # # 🔹 Custom Agent Classes
# # # =========================

# # class PDFExtractorAgent:
# #     def __init__(self):
# #         pass

# #     def extract(self, file_path: str) -> str:
# #         doc = fitz.open(file_path)
# #         text = ""
# #         for page in doc:
# #             text += page.get_text()
# #         return text

# # class TopicGeneratorAgent:
# #     def __init__(self):
# #         pass

# #     def generate(self, content: str) -> list:
# #         # Dummy logic for now
# #         return ["Topic 1", "Topic 2", "Topic 3"]

# # class SessionGeneratorAgent:
# #     def __init__(self):
# #         pass

# #     def generate_sessions(self, topic: str) -> list:
# #         # Dummy logic
# #         return [f"{topic} - Session 1", f"{topic} - Session 2"]

# # class EpisodeGeneratorAgent:
# #     def __init__(self):
# #         pass

# #     def generate_episodes(self, session: str) -> list:
# #         # Dummy logic
# #         return [f"{session} - Episode 1", f"{session} - Episode 2"]

# # class ScriptGeneratorAgent:
# #     def __init__(self):
# #         pass

# #     def generate_script(self, episode: str) -> str:
# #         # Dummy logic
# #         return f"Generated script for {episode}"


# # # LLM/agents.py
# # from langchain.agents import initialize_agent, Tool
# # from langchain_groq import ChatGroq
# # from langchain.agents.agent_types import AgentType
# # # Load the Groq LLM
# # llm = ChatGroq(
# #     model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
# #     temperature=0
# # )
# # # Define a basic tool for testing
# # def echo_tool(input_text: str) -> str:
# #     return f"You said: {input_text}"
# # tools = [
# #     Tool(
# #         name="EchoTool",
# #         func=echo_tool,
# #         description="Repeats what the user says for testing purposes."
# #     )
# # ]
# # # Initialize the agent
# # agent_executor = initialize_agent(
# #     tools=tools,
# #     llm=llm,
# #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# #     verbose=True
# # )
# # # Function to run the agent with a user prompt
# # def run_agent(prompt: str) -> str:
# #     return agent_executor.run(prompt)
# # # agents.py
# # class PDFExtractorAgent:
# #     def __init__(self):
# #         pass
# #     def extract(self, file_path: str) -> str:
# #         # Simple example using PyMuPDF
# #         import fitz  # PyMuPDF
# #         doc = fitz.open(file_path)
# #         text = ""
# #         for page in doc:
# #             text += page.get_text()
# #         return text
# # LLM/agents.py
# # LLM/agents.py
# from langchain.agents import initialize_agent, Tool
# from langchain_groq import ChatGroq
# from langchain.agents.agent_types import AgentType
# import fitz  # PyMuPDF
# from langchain.output_parsers import PydanticOutputParser
# from langchain.prompts import PromptTemplate
# from pydantic import BaseModel
# from typing import List

# # =========================
# # :small_blue_diamond: LLM Initialization
# # =========================
# def load_llm():
#     return ChatGroq(
#         model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
#         temperature=0
#     )
# # =========================
# # :small_blue_diamond: Tools
# # =========================
# def echo_tool(input_text: str) -> str:
#     return f"You said: {input_text}"
# def get_tools():
#     return [
#         Tool(
#             name="EchoTool",
#             func=echo_tool,
#             description="Repeats what the user says for testing purposes."
#         )
#     ]
# # =========================
# # :small_blue_diamond: Agent Executor
# # =========================
# def initialize_echo_agent():
#     llm = load_llm()
#     tools = get_tools()
#     return initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True
#     )
# def run_agent(prompt: str) -> str:
#     agent_executor = initialize_echo_agent()
#     return agent_executor.run(prompt)
# # =========================
# # :small_blue_diamond: Custom Agent Classes
# # =========================
# class PDFExtractorAgent:
#     def __init__(self):
#         pass
#     def extract(self, file_path: str) -> str:
#         doc = fitz.open(file_path)
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         return text
# class Episode(BaseModel):
#     title: str
#     description: str

# class Session(BaseModel):
#     title: str
#     description: str
#     episodes: List[Episode]

# class Topic(BaseModel):
#     title: str
#     description: str
#     sessions: List[Session]

# class LearningStructure(BaseModel):
#     summary: str
#     topics: List[Topic]

# # class TopicGeneratorAgent:
# #     def __init__(self):
# #         self.llm = load_llm()

# #     def generate(self, content: str) -> dict:
# #         parser = PydanticOutputParser(pydantic_object=LearningStructure)

# #         prompt_template = PromptTemplate(
# #             template="""
# # You are an expert educational content analyzer. Analyze the following document and extract a hierarchical learning structure.

# # Your task is to:
# # 1. Identify main topics/themes in the document
# # 2. For each topic, break it down into logical learning sessions
# # 3. For each session, identify specific episodes or learning units
# # 4. Provide a brief summary of the entire document

# # Guidelines:
# # - Topics should be broad themes or subject areas
# # - Sessions should be logical groupings within topics (like chapters or modules)
# # - Episodes should be specific learning units or subtopics within sessions
# # - Each level should have a clear title and description
# # - Aim for 2–5 topics, 2–4 sessions per topic, and 2–6 episodes per session
# # - Descriptions should be informative and educational

# # {format_instructions}

# # Content:
# # {content}
# # """,
# #             input_variables=["content"],
# #             partial_variables={"format_instructions": parser.get_format_instructions()}
# #         )

# #         chain = prompt_template | self.llm | parser
# #         result = chain.invoke({"content": content})
# #         return result.dict()
# from typing import Dict, List, Optional
# import json



# # class TopicGeneratorAgent:
# def __init__(self):
#         self.llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# def generate(self, raw_text: str) -> Dict:
#         prompt = f"""
# You are an expert educational content analyzer. Analyze the following document and extract a hierarchical learning structure.

# Your task is to:
# 1. Identify main topics/themes in the document
# 2. For each topic, break it down into logical learning sessions
# 3. For each session, identify specific episodes or learning units
# 4. Provide a brief summary of the entire document

# Format the output as valid JSON in the following format:
# {{
#   "summary": "Brief summary here",
#   "topics": [
#     {{
#       "title": "Topic Title",
#       "description": "Topic Description",
#       "sessions": [
#         {{
#           "title": "Session Title",
#           "description": "Session Description",
#           "episodes": [
#             {{
#               "title": "Episode Title",
#               "description": "Episode Description"
#             }}
#           ]
#         }}
#       ]
#     }}
#   ]
# }}

# Only return valid JSON. Do not include anything else.

# Document:
# {raw_text[:8000]}
# """

#         response = self.llm.invoke(prompt)
#         try:
#             return json.loads(response.content.strip())
#         except json.JSONDecodeError as e:
#             return {
#                 "error": "Invalid JSON returned from model",
#                 "raw_response": response.content,
#                 "exception": str(e)
#             }


# class SessionGeneratorAgent:
#     def __init__(self):
#         pass
#     def generate_sessions(self, topic: str) -> list:
#         # Dummy logic
#         return [f"{topic} - Session 1", f"{topic} - Session 2"]
# class EpisodeGeneratorAgent:
#     def __init__(self):
#         pass
#     def generate_episodes(self, session: str) -> list:
#         # Dummy logic
#         return [f"{session} - Episode 1", f"{session} - Episode 2"]
# class ScriptGeneratorAgent:
#     def __init__(self):
#         pass
#     def generate_script(self, episode: str) -> str:
#         # Dummy logic
#         return f"Generated script for {episode}"



#--------------------------------------------------------#

# LLM/agents.py

from typing import List, Dict
import json
import fitz  # PyMuPDF
from pydantic import BaseModel
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq

# =========================
# 🔹 LLM Initialization
# =========================
def load_llm():
    return ChatGroq(
        model="llama3-8b-8192",
        temperature=0
    )

# =========================
# 🔹 Agent Executor for Echo Tool
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

def initialize_echo_agent():
    return initialize_agent(
        tools=get_tools(),
        llm=load_llm(),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

def run_agent(prompt: str) -> str:
    return initialize_echo_agent().run(prompt)

# =========================
# 🔹 Pydantic Data Models
# =========================
class Episode(BaseModel):
    title: str
    description: str

class Session(BaseModel):
    title: str
    description: str
    episodes: List[Episode]

class Topic(BaseModel):
    title: str
    description: str
    sessions: List[Session]

class LearningStructure(BaseModel):
    summary: str
    topics: List[Topic]

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
        self.llm = load_llm()

    def generate(self, raw_text: str) -> Dict:
        prompt = f"""
You are an expert educational content analyzer. Analyze the following document and extract a hierarchical learning structure.

Your task is to:
1. Identify main topics/themes in the document
2. For each topic, break it down into logical learning sessions
3. For each session, identify specific episodes or learning units
4. Provide a brief summary of the entire document

Format the output as valid JSON in the following format:
{{
  "summary": "Brief summary here",
  "topics": [
    {{
      "title": "Topic Title",
      "description": "Topic Description",
      "sessions": [
        {{
          "title": "Session Title",
          "description": "Session Description",
          "episodes": [
            {{
              "title": "Episode Title",
              "description": "Episode Description"
            }}
          ]
        }}
      ]
    }}
  ]
}}

Only return valid JSON. Do not include anything else.

Document:
{raw_text[:8000]}
"""
        response = self.llm.invoke(prompt)
        try:
            return json.loads(response.content.strip())
        except json.JSONDecodeError as e:
            return {
                "error": "Invalid JSON returned from model",
                "raw_response": response.content,
                "exception": str(e)
            }


class SessionGeneratorAgent:
    def __init__(self):
        pass

    def generate_sessions(self, topic: str) -> List[str]:
        # Placeholder logic
        return [f"{topic} - Session 1", f"{topic} - Session 2"]


class EpisodeGeneratorAgent:
    def __init__(self):
        pass

    def generate_episodes(self, session: str) -> List[str]:
        # Placeholder logic
        return [f"{session} - Episode 1", f"{session} - Episode 2"]


class ScriptGeneratorAgent:
    def __init__(self):
        pass

    def generate_script(self, episode: str) -> str:
        # Placeholder logic
        return f"Generated script for {episode}"

#-----------------------------------------------------------------------------#
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
import fitz  # PyMuPDF
# =========================
# :small_blue_diamond: LLM Initialization
# =========================
def load_llm():
    return ChatGroq(
        model="llama3-8b-8192",  # You can also try "mixtral-8x7b-32768"
        temperature=0
    )
# =========================
# :small_blue_diamond: Tools
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
# :small_blue_diamond: Agent Executor
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
# :small_blue_diamond: Custom Agent Classes
# =========================
class PDFExtractorAgent:
    def __init__(self):
        pass
    def extract(self, file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}")
class TopicGeneratorAgent:
    def __init__(self):
        pass
    def generate(self, content: str) -> list:
        # Placeholder logic; replace with LLM or rule-based generation as needed
        return ["Topic 1: Introduction", "Topic 2: Core Concepts", "Topic 3: Advanced Applications"]
class SessionGeneratorAgent:
    def __init__(self):
        pass
    def generate_sessions(self, topic: str) -> list:
        return [f"{topic} - Session 1: Overview", f"{topic} - Session 2: Deep Dive"]
class EpisodeGeneratorAgent:
    def __init__(self):
        pass
    def generate_episodes(self, session: str) -> list:
        return [f"{session} - Episode 1: Basics", f"{session} - Episode 2: Examples"]
class ScriptGeneratorAgent:
    def __init__(self):
        pass
    def generate_script(self, episode: str) -> str:
        return f"This is the script content for {episode}. Add LLM logic here for auto-generation."






