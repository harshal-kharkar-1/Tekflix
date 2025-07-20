# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import json
import logging

from .models import ContentProject, Topic, Session, Episode, ProcessingLog
from .services import ContentGenerationService
from .forms import ContentProjectForm  # We'll create this

logger = logging.getLogger(__name__)

def project_list(request):
    """List all content projects"""
    projects = ContentProject.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'LLM/project_list.html', context)

def project_detail(request, project_id):
    """View project details with topics, sessions, and episodes"""
    project = get_object_or_404(ContentProject, id=project_id)
    topics = project.topics.prefetch_related('sessions__episodes').all()
    logs = project.logs.all()[:50]  # Show recent logs
    
    context = {
        'project': project,
        'topics': topics,
        'logs': logs,
    }
    return render(request, 'LLM/project_detail.html', context)

def create_project(request):
    """Create a new content project"""
    if request.method == 'POST':
        form = ContentProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ContentProjectForm()
    
    return render(request, 'LLM/create_project.html', {'form': form})

@csrf_exempt
@require_http_methods(["POST"])
def process_project(request, project_id):
    """API endpoint to start processing a project"""
    try:
        project = get_object_or_404(ContentProject, id=project_id)
        
        if not project.pdf_file:
            return JsonResponse({
                'success': False, 
                'error': 'No PDF file uploaded'
            }, status=400)
        
        if project.status == 'processing':
            return JsonResponse({
                'success': False, 
                'error': 'Project is already being processed'
            }, status=400)
        
        # Start processing in background (you might want to use Celery for this)
        service = ContentGenerationService()
        result = service.process_pdf(project_id)
        
        return JsonResponse(result)
        
    except Exception as e:
        logger.error(f"Error processing project {project_id}: {e}")
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def project_status(request, project_id):
    """API endpoint to check project status"""
    project = get_object_or_404(ContentProject, id=project_id)
    
    return JsonResponse({
        'status': project.status,
        'topics_count': project.topics.count(),
        'sessions_count': sum(topic.sessions.count() for topic in project.topics.all()),
        'episodes_count': sum(
            session.episodes.count() 
            for topic in project.topics.all() 
            for session in topic.sessions.all()
        ),
    })

def export_project(request, project_id):
    """Export project as JSON"""
    project = get_object_or_404(ContentProject, id=project_id)
    
    # Build the export structure
    data = {
        'project': {
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
        },
        'topics': []
    }
    
    for topic in project.topics.all():
        topic_data = {
            'title': topic.title,
            'description': topic.description,
            'sessions': []
        }
        
        for session in topic.sessions.all():
            session_data = {
                'title': session.title,
                'description': session.description,
                'episodes': []
            }
            
            for episode in session.episodes.all():
                episode_data = {
                    'title': episode.title,
                    'description': episode.description,
                    'script': episode.script,
                    'duration_minutes': episode.duration_minutes,
                }
                session_data['episodes'].append(episode_data)
            
            topic_data['sessions'].append(session_data)
        
        data['topics'].append(topic_data)
    
    response = JsonResponse(data, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="project_{project.id}_export.json"'
    
    return response

from .services import extract_text_from_file, generate_structure_from_text

def create_project(request):
    if request.method == 'POST':
        form = ContentProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)

            uploaded_file = request.FILES.get('pdf_file')
            if uploaded_file:
                raw_text = extract_text_from_file(uploaded_file)
                project.raw_text = raw_text

            project.save()

            # 🧠 Generate topic/session/episode structure
            generate_structure_from_text(project)

            messages.success(request, f'Project "{project.name}" created and processed successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ContentProjectForm()

    return render(request, 'LLM/create_project.html', {'form': form})
