from langchain_groq import ChatGroq
from dotenv import load_dotenv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")




import os
import shutil
import tempfile
import logging
import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
from typing import List, Dict, TypedDict
from django.views.decorators.http import require_http_methods

load_dotenv()
logger = logging.getLogger(__name__)


# Define schema models
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
        model="llama3-8b-8192",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

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
        - Sessions should be logical groupings within topics
        - Episodes should be specific learning units
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




from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
import tempfile, shutil, os
import logging

logger = logging.getLogger(__name__)
