import os
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
import json
import logging
from langchain_core.utils import pre_init
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define schema
class Episode(BaseModel):
    title: str = Field(..., description="The episode title")
    description: str = Field(..., description="Detailed description of the episode content")

class Session(BaseModel):
    title: str = Field(..., description="The session title")
    description: str = Field(..., description="Detailed description of the session")
    episodes: List[Episode] = Field(default_factory=list, description="List of episodes in this session")

class Topic(BaseModel):
    title: str = Field(..., description="The topic title")
    description: str = Field(..., description="Detailed description of the topic")
    sessions: List[Session] = Field(default_factory=list, description="List of sessions in this topic")

class HierarchicalResponse(BaseModel):
    topics: List[Topic] = Field(..., description="List of topics with their hierarchical structure")
    document_summary: str = Field(..., description="Overall summary of the document")

class GraphState(TypedDict):
    text: str
    result: HierarchicalResponse

# Load PDF
def load_pdf(file_path: str) -> str:
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text = "\n\n--- PAGE BREAK ---\n\n".join(page.page_content for page in pages)
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading PDF: {str(e)}")

# Extract Topics
def extract_hierarchical_topics(text: str) -> HierarchicalResponse:
    try:
        # llm = ChatGroq(
        #     model="llama3-8b-8192",
        #     temperature=0.1,
        #     api_key=GROQ_API_KEY

        # )
        llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        print("GROQ API", os.getenv("GROQ_API_KEY"))


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
            - Aim for 2-5 topics, 2-4 sessions per topic, and 2-6 episodes per session
            - Descriptions should be informative and educational

            Return your analysis in the following JSON format:
            {parser.get_format_instructions()}

            Document Text:
            {text_sample}
            """
            print(f"propt {prompt}")
            response = llm.invoke(prompt)
            try:
                result = parser.parse(response.content)
                return {"text": state["text"], "result": result}
            except Exception as parse_error:
                raise HTTPException(status_code=500, detail=f"Error parsing LLM response: {str(parse_error)}")

        # LangGraph pipeline
        workflow = StateGraph(GraphState)
        workflow.add_node("analyze", analyze_document_node)
        workflow.set_entry_point("analyze")
        workflow.set_finish_point("analyze")

        app_graph = workflow.compile()
        result = app_graph.invoke({"text": text})
        return result["result"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting hierarchical topics: {str(e)}")

# 🆕 Output Formatter
def convert_to_separate_topic_dicts(response: HierarchicalResponse) -> List[Dict]:
    """Return a list of separate topic JSON objects (one per topic)"""
    topic_dicts = []
    
    for topic_index, topic in enumerate(response.topics, start=1):
        topic_key = f"Topic {topic_index}"
        topic_obj = {
            topic_key: {
                "title": topic.title,
                "description": topic.description,
                "sessions": {}
            }
        }

        for session_index, session in enumerate(topic.sessions, start=1):
            session_key = f"Session {session_index}"
            session_obj = {
                "title": session.title,
                "description": session.description,
                "episodes": {}
            }

            for episode_index, episode in enumerate(session.episodes, start=1):
                episode_key = f"Episode {episode_index}"
                session_obj["episodes"][episode_key] = {
                    "title": episode.title,
                    "description": episode.description
                }

            topic_obj[topic_key]["sessions"][session_key] = session_obj
        
        topic_dicts.append(topic_obj)
    
    return topic_dicts


# FastAPI app setup
app = FastAPI(
    title="Hierarchical PDF Topic Extractor",
    version="2.0.0",
    description="Extract hierarchical learning structure from PDF documents"
)

@app.get("/")
async def root():
    return {
        "message": "Hierarchical PDF Topic Extractor API",
        "version": "2.0.0",
        "description": "Upload a PDF to extract topics, sessions, and episodes in a hierarchical structure"
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_file_path = tmp_file.name

    try:
        text = load_pdf(tmp_file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        result = extract_hierarchical_topics(text)
        nested_structure = convert_to_separate_topic_dicts(result)

        return {
            "success": True,
            "filename": file.filename,
            "document_summary": result.document_summary,
            "topics": [topic.dict() for topic in result.topics],
            "nested_structure": nested_structure,
            "stats": {
                "total_topics": len(result.topics),
                "total_sessions": sum(len(topic.sessions) for topic in result.topics),
                "total_episodes": sum(len(session.episodes) for topic in result.topics for session in topic.sessions)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/schema")
async def get_schema():
    return {
        "hierarchical_response": HierarchicalResponse.schema(),
        "nested_format_example": {
            "Topic 1": {
                "title": "Sample Topic",
                "description": "Description of topic",
                "sessions": {
                    "Session 1": {
                        "title": "Sample Session",
                        "description": "Description of session",
                        "episodes": {
                            "Episode 1": {
                                "title": "Sample Episode",
                                "description": "Description of episode"
                            }
                        }
                    }
                }
            }
        }
    }

@app.on_event("startup")
async def startup_event():
    if not os.getenv("GROQ_API_KEY"):
        logger.warning("GROQ_API_KEY environment variable not set. Make sure to set it before processing requests.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, log_level="info")
