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
from .services import ContentGenerationService, extract_text_from_file, generate_structure_from_text
from .forms import ContentProjectForm

logger = logging.getLogger(__name__)

def project_list(request):
    projects = ContentProject.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'LLM/project_list.html', context)


def project_detail(request, pk):
    project = get_object_or_404(ContentProject, pk=pk)

    structured_data = {}

    for topic in project.topics.all():
        category = topic.category.name if hasattr(topic, 'category') and topic.category else 'Uncategorized'

        if category not in structured_data:
            structured_data[category] = {}

        topic_data = {
            'description': topic.description,
            'sessions': {}
        }

        for session in topic.sessions.all():
            session_data = {
                'description': session.description,
                'episodes': {}
            }

            for episode in session.episodes.all():
                session_data['episodes'][episode.title] = {
                    'description': episode.description
                }

            topic_data['sessions'][session.title] = session_data

        structured_data[category][topic.title] = topic_data

    return JsonResponse(structured_data, safe=False, json_dumps_params={'indent': 4})


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

            generate_structure_from_text(project)

            messages.success(request, f'Project "{project.name}" created and processed successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ContentProjectForm()

    return render(request, 'LLM/create_project.html', {'form': form})


@csrf_exempt
@require_http_methods(["POST"])
def process_project(request, pk):
    try:
        project = get_object_or_404(ContentProject, pk=pk)

        if not project.pdf_file:
            return JsonResponse({'success': False, 'error': 'No PDF file uploaded'}, status=400)

        if project.status == 'processing':
            return JsonResponse({'success': False, 'error': 'Project is already being processed'}, status=400)

        service = ContentGenerationService()
        result = service.process_pdf(pk)

        return JsonResponse(result)

    except Exception as e:
        logger.error(f"Error processing project {pk}: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
def project_status(request, pk):
    project = get_object_or_404(ContentProject, pk=pk)

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


def export_project(request, pk):
    project = get_object_or_404(ContentProject, pk=pk)

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
                session_data['episodes'].append({
                    'title': episode.title,
                    'description': episode.description,
                    'script': episode.script,
                    'duration_minutes': episode.duration_minutes,
                })

            topic_data['sessions'].append(session_data)

        data['topics'].append(topic_data)

    response = JsonResponse(data, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="project_{project.id}_export.json"'

    return response

from django.http import JsonResponse
from LLM.agents import TopicGeneratorAgent, PDFExtractorAgent

# def generate_topic_view(request):
#     file_path = "media/pdfs/sample.pdf"  # replace with actual uploaded file path
#     extractor = PDFExtractorAgent()
#     content = extractor.extract(file_path)

#     topic_agent = TopicGeneratorAgent()
#     result = topic_agent.generate(content)

#     return JsonResponse(result)
def generate_topic_view(request):
    file_path = "media/pdfs/sample.pdf"  # Change path if needed

    extractor = PDFExtractorAgent()
    content = extractor.extract(file_path)

    topic_agent = TopicGeneratorAgent()
    result = topic_agent.generate(content)

    # Debugging: Check if there's an error from the LLM
    if "error" in result:
        return JsonResponse({"success": False, "error": result["error"], "raw": result["raw_response"]}, status=500)

    return JsonResponse(result, json_dumps_params={'indent': 2})
