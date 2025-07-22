import os
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.core.files.storage import default_storage
from .models import ContentProject, Topic as TopicModel, Session as SessionModel, Episode as EpisodeModel, ProcessingLog
from .langgraph_workflow import AutoGraphWorkflow  # We'll create this

from .models import Topic, Session, Episode
# from .utils import chunk_text


from .utils.pdf_loader import chunk_text




def generate_structure_from_text(project):
    chunks = chunk_text(project.raw_text, chunk_size=1000)

    for i, chunk in enumerate(chunks):
        topic = Topic.objects.create(
            project=project,
            title=f"Topic {i + 1}",
            description=f"This topic is about: {chunk[:100]}"
        )

        session = Session.objects.create(
            topic=topic,
            title=f"Session {i + 1}",
            description="Auto-generated session content."
        )

        Episode.objects.create(
            session=session,
            title=f"Episode {i + 1}",
            description="Auto-generated episode content.",
            script=chunk[:500],
            duration_minutes=5
        )


logger = logging.getLogger(__name__)

class ContentGenerationService:
    """Service to handle content generation using LangGraph"""
    
    def __init__(self):
        self.workflow = AutoGraphWorkflow()
    
    def process_pdf(self, project_id: int) -> Dict[str, Any]:
        """Process a PDF and generate content structure"""
        try:
            project = ContentProject.objects.get(id=project_id)
            project.status = 'processing'
            project.save()
            
            self._log(project, 'info', 'Starting PDF processing')
            
            # Get the file path
            pdf_path = project.pdf_file.path
            
            # Run the LangGraph workflow
            result = self.workflow.run_workflow(
                pdf_path=pdf_path,
                output_path=f"output_{project.id}.json"
            )
            
            if result.get('error'):
                self._log(project, 'error', f"Workflow failed: {result['error']}")
                project.status = 'failed'
                project.save()
                return {'success': False, 'error': result['error']}
            
            # Save the generated structure to database
            self._save_structure_to_db(project, result)
            
            project.status = 'completed'
            project.save()
            
            self._log(project, 'info', 'Content generation completed successfully')
            
            return {'success': True, 'project_id': project.id}
            
        except Exception as e:
            logger.error(f"Error processing project {project_id}: {e}")
            project.status = 'failed'
            project.save()
            self._log(project, 'error', f"Processing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _save_structure_to_db(self, project: ContentProject, result: Dict[str, Any]):
        """Save the generated structure to Django models"""
        topics_data = result.get('topics', [])
        
        for topic_idx, topic_data in enumerate(topics_data):
            # Create topic
            topic = TopicModel.objects.create(
                project=project,
                title=topic_data['title'],
                description=topic_data['description'],
                order=topic_idx
            )
            
            # Create sessions for this topic
            sessions_data = topic_data.get('sessions', [])
            for session_idx, session_data in enumerate(sessions_data):
                session = SessionModel.objects.create(
                    topic=topic,
                    title=session_data['title'],
                    description=session_data['description'],
                    order=session_idx
                )
                
                # Create episodes for this session
                episodes_data = session_data.get('episodes', [])
                for episode_idx, episode_data in enumerate(episodes_data):
                    EpisodeModel.objects.create(
                        session=session,
                        title=episode_data['title'],
                        description=episode_data['description'],
                        script=episode_data.get('script', ''),
                        duration_minutes=episode_data.get('duration_minutes'),
                        order=episode_idx
                    )
    
    def _log(self, project: ContentProject, level: str, message: str):
        """Log a message to the database"""
        ProcessingLog.objects.create(
            project=project,
            step='content_generation',
            message=message,
            level=level
        )

from .utils.pdf_loader import extract_text_from_pdf

def extract_text_from_file(file_path):
    return extract_text_from_pdf(file_path)


import tempfile

def extract_text_from_file(uploaded_file):
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        for chunk in uploaded_file.chunks():
            temp.write(chunk)
        temp_path = temp.name

    # Now extract text using the file path
    return extract_text_from_pdf(temp_path)
