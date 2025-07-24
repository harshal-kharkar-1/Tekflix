import os
import tempfile
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from a .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


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

class HierarchicalResponse(BaseModel):
    topics: List[Topic]
    document_summary: str

class GraphState(TypedDict):
    text: str
    result: HierarchicalResponse


def load_pdf(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return "\n\n--- PAGE BREAK ---\n\n".join(page.page_content for page in pages)


def extract_hierarchical_topics(text: str) -> HierarchicalResponse:
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.1,
        api_key=GROQ_API_KEY,
    )
    print("🔑 Using Groq API key:", GROQ_API_KEY)  # Mask most of it for safety
    print(f"LLLLLLLLLL{llm}")

    parser = PydanticOutputParser(pydantic_object=HierarchicalResponse)

    def analyze_document_node(state: GraphState) -> GraphState:
        text_sample = state['text'][:8000]
        prompt = f"""
        You are an expert educational content analyzer. Analyze the following document and extract a hierarchical learning structure.

        Your task is to:
        1. Identify main topics/themes in the document
        2. For each topic, break it down into logical learning sessions
        3. For each session, identify specific episodes or learning units
        4. Provide a brief summary of the entire document

        Guidelines:
        - Topics should be broad themes or subject areas
        - Sessions should be logical groupings within topics (like chapters or modules)
        - Episodes should be specific learning units or subtopics within sessions
        - Each level should have a clear title and description
        - Return in JSON format like this: {parser.get_format_instructions()}

        Document Text:
        {text_sample}
        """
        response = llm.invoke(prompt)
        return {"text": state["text"], "result": parser.parse(response.content)}

    workflow = StateGraph(GraphState)
    workflow.add_node("analyze", analyze_document_node)
    workflow.set_entry_point("analyze")
    workflow.set_finish_point("analyze")
    result = workflow.compile().invoke({"text": text})
    return result["result"]


def convert_to_separate_topic_dicts(response: HierarchicalResponse) -> List[Dict]:
    topic_dicts = []
    for i, topic in enumerate(response.topics, 1):
        topic_obj = {
            f"Topic {i}": {
                "title": topic.title,
                "description": topic.description,
                "sessions": {}
            }
        }
        for j, session in enumerate(topic.sessions, 1):
            session_obj = {
                "title": session.title,
                "description": session.description,
                "episodes": {
                    f"Episode {k+1}": {
                        "title": e.title,
                        "description": e.description
                    } for k, e in enumerate(session.episodes)
                }
            }
            topic_obj[f"Topic {i}"]["sessions"][f"Session {j}"] = session_obj
        topic_dicts.append(topic_obj)
    return topic_dicts
