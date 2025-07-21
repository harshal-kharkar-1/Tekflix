# import os
# import json
# from pathlib import Path
# from typing import Dict, List, Optional, Any
# import logging
# from django.conf import settings

# # Import your existing classes (copy them here or import from another module)
# from .agents import (
#     PDFExtractorAgent, 
#     TopicGeneratorAgent, 
#     SessionGeneratorAgent, 
#     EpisodeGeneratorAgent,
#     ScriptGeneratorAgent
# )
# from .models_langgraph import AutoGraphState  # Your existing state model

# from langgraph.graph import StateGraph, END, START
# # from langchain_openai import ChatOpenAI

# logger = logging.getLogger(__name__)
# from langchain_groq import ChatGroq

# class AutoGraphWorkflow:
#     """Django-integrated LangGraph workflow"""
#     self.llm = ChatGroq(
#     model="mixtral-8x7b-32768",  # or "llama3-70b-8192", etc., based on your choice
#     temperature=0.1,
#     api_key=settings.GROQ_API_KEY  # Make sure to set this in your Django settings
# )
        
#         # Initialize agents
#         self.pdf_extractor = PDFExtractorAgent()
#         self.topic_generator = TopicGeneratorAgent(self.llm)
#         self.session_generator = SessionGeneratorAgent(self.llm)
#         self.episode_generator = EpisodeGeneratorAgent(self.llm)
#         self.script_generator = ScriptGeneratorAgent(self.llm)
        
#         # Build the graph
#         self.graph = self._build_graph()
    
#     def _build_graph(self) -> StateGraph:
#         """Build the LangGraph workflow"""
#         workflow = StateGraph(AutoGraphState)
        
#         # Add nodes
#         workflow.add_node("extract_pdf", self.pdf_extractor.extract_text)
#         workflow.add_node("generate_topics", self.topic_generator.generate_topics)
#         workflow.add_node("process_topic", self._process_single_topic)
#         workflow.add_node("generate_sessions", self.session_generator.generate_sessions)
#         workflow.add_node("process_session", self._process_single_session)
#         workflow.add_node("generate_episodes", self.episode_generator.generate_episodes)
#         workflow.add_node("process_episode", self._process_single_episode)
#         workflow.add_node("generate_script", self.script_generator.generate_script)
#         workflow.add_node("finalize", self._finalize_structure)
        
#         # Add edges (your existing logic)
#         workflow.add_edge(START, "extract_pdf")
#         workflow.add_edge("extract_pdf", "generate_topics")
#         workflow.add_edge("generate_topics", "process_topic")
#         # ... add all your existing edges
        
#         return workflow.compile()
    
#     def run_workflow(self, pdf_path: str, output_path: str) -> Dict[str, Any]:
#         """Run the complete workflow"""
#         initial_state = {
#             "pdf_path": pdf_path,
#             "output_path": output_path,
#             "messages": [],
#             "topics": [],
#             "current_topic_index": 0,
#             "current_session_index": 0,
#             "current_episode_index": 0,
#         }
        
#         try:
#             result = self.graph.invoke(initial_state)
#             return result
#         except Exception as e:
#             logger.error(f"Workflow execution failed: {e}")
#             return {"error": str(e)}
    
#     # Add your existing helper methods here
#     def _process_single_topic(self, state: AutoGraphState) -> AutoGraphState:
#         # Your existing implementation
#         pass
    
#     # ... other methods

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from django.conf import settings

# Import your existing classes (copy them here or import from another module)
from .agents import (
    PDFExtractorAgent, 
    TopicGeneratorAgent, 
    SessionGeneratorAgent, 
    EpisodeGeneratorAgent,
    ScriptGeneratorAgent
)
from .models_langgraph import AutoGraphState  # Your existing state model

from langgraph.graph import StateGraph, END, START
from langchain_groq import ChatGroq  # ✅ Using Groq now

logger = logging.getLogger(__name__)

class AutoGraphWorkflow:
    """Django-integrated LangGraph workflow"""

    def __init__(self):
        self.llm = ChatGroq(
            model="mixtral-8x7b-32768",  # or "llama3-70b-8192"
            temperature=0.1,
            api_key=settings.GROQ_API_KEY  # ✅ Load from settings
        )
        
        # Initialize agents
        self.pdf_extractor = PDFExtractorAgent()
        self.topic_generator = TopicGeneratorAgent(self.llm)
        self.session_generator = SessionGeneratorAgent(self.llm)
        self.episode_generator = EpisodeGeneratorAgent(self.llm)
        self.script_generator = ScriptGeneratorAgent(self.llm)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AutoGraphState)
        
        # Add nodes
        workflow.add_node("extract_pdf", self.pdf_extractor.extract_text)
        workflow.add_node("generate_topics", self.topic_generator.generate_topics)
        workflow.add_node("process_topic", self._process_single_topic)
        workflow.add_node("generate_sessions", self.session_generator.generate_sessions)
        workflow.add_node("process_session", self._process_single_session)
        workflow.add_node("generate_episodes", self.episode_generator.generate_episodes)
        workflow.add_node("process_episode", self._process_single_episode)
        workflow.add_node("generate_script", self.script_generator.generate_script)
        workflow.add_node("finalize", self._finalize_structure)
        
        # Add edges (you can update more here)
        workflow.add_edge(START, "extract_pdf")
        workflow.add_edge("extract_pdf", "generate_topics")
        workflow.add_edge("generate_topics", "process_topic")
        workflow.add_edge("generate_script", "finalize")
        workflow.add_edge("finalize", END)

        # Add more edges as per your flow
        
        return workflow.compile()
    
    def run_workflow(self, pdf_path: str, output_path: str) -> Dict[str, Any]:
        """Run the complete workflow"""
        initial_state = {
            "pdf_path": pdf_path,
            "output_path": output_path,
            "messages": [],
            "topics": [],
            "current_topic_index": 0,
            "current_session_index": 0,
            "current_episode_index": 0,
        }
        
        try:
            result = self.graph.invoke(initial_state)
            return result
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {"error": str(e)}
    
    def _process_single_topic(self, state: AutoGraphState) -> AutoGraphState:
        # Your existing implementation
        pass

    # Add other helper methods here
