# # from django.shortcuts import render

# # # Create your views here.
# # from django.http import HttpResponse


# # def index(request):
# #     return HttpResponse("Hello, world. You're at the polls index.")


# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.db.models import Q
# import json
# import logging


# from .models import ContentProject, Topic, Session, Episode, ProcessingLog
# from .services import ContentGenerationService
# from .forms import ContentProjectForm  # We'll create this

# logger = logging.getLogger(__name__)

# def project_list(request):
#     """List all content projects"""
#     projects = ContentProject.objects.all().order_by('-created_at')
    
#     # Search functionality
#     search_query = request.GET.get('search', '')
#     if search_query:
#         projects = projects.filter(
#             Q(name__icontains=search_query) | 
#             Q(description__icontains=search_query)
#         )
    
#     # Pagination
#     paginator = Paginator(projects, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         'page_obj': page_obj,
#         'search_query': search_query,
#     }
#     return render(request, 'LLM/project_list.html', context)

# # def project_detail(request, project_id):
# #     """View project details with topics, sessions, and episodes"""
# #     project = get_object_or_404(ContentProject, id=project_id)
# #     topics = project.topics.prefetch_related('sessions__episodes').all()
# #     logs = project.logs.all()[:50]  # Show recent logs
    
# #     context = {
# #         'project': project,
# #         'topics': topics,
# #         'logs': logs,
# #     }
# #     return render(request, 'LLM/project_detail.html', context)

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import Project  # update with your actual model path

# def project_detail(request, pk):
#     project = get_object_or_404(Project, pk=pk)

#     structured_data = {}

#     for topic in project.topics.all():
#         category = topic.category.name if hasattr(topic, 'category') and topic.category else 'Uncategorized'

#         if category not in structured_data:
#             structured_data[category] = {}

#         topic_data = {
#             'description': topic.description,
#             'sessions': {}
#         }

#         for session in topic.sessions.all():
#             session_data = {
#                 'description': session.description,
#                 'episodes': {}
#             }

#             for episode in session.episodes.all():
#                 session_data['episodes'][episode.title] = {
#                     'description': episode.description
#                 }

#             topic_data['sessions'][session.title] = session_data

#         structured_data[category][topic.title] = topic_data

#     return JsonResponse(structured_data, safe=False, json_dumps_params={'indent': 4})

# def create_project(request):
#     """Create a new content project"""
#     if request.method == 'POST':
#         form = ContentProjectForm(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save()
#             messages.success(request, f'Project "{project.name}" created successfully!')
#             return redirect('project_detail', project_id=project.id)
#     else:
#         form = ContentProjectForm()
    
#     return render(request, 'LLM/create_project.html', {'form': form})

# @csrf_exempt
# @require_http_methods(["POST"])
# def process_project(request, project_id):
#     """API endpoint to start processing a project"""
#     try:
#         project = get_object_or_404(ContentProject, id=project_id)
        
#         if not project.pdf_file:
#             return JsonResponse({
#                 'success': False, 
#                 'error': 'No PDF file uploaded'
#             }, status=400)
        
#         if project.status == 'processing':
#             return JsonResponse({
#                 'success': False, 
#                 'error': 'Project is already being processed'
#             }, status=400)
        
#         # Start processing in background (you might want to use Celery for this)
#         service = ContentGenerationService()
#         result = service.process_pdf(project_id)
        
#         return JsonResponse(result)
        
#     except Exception as e:
#         logger.error(f"Error processing project {project_id}: {e}")
#         return JsonResponse({
#             'success': False, 
#             'error': str(e)
#         }, status=500)

# @require_http_methods(["GET"])
# def project_status(request, project_id):
#     """API endpoint to check project status"""
#     project = get_object_or_404(ContentProject, id=project_id)
    
#     return JsonResponse({
#         'status': project.status,
#         'topics_count': project.topics.count(),
#         'sessions_count': sum(topic.sessions.count() for topic in project.topics.all()),
#         'episodes_count': sum(
#             session.episodes.count() 
#             for topic in project.topics.all() 
#             for session in topic.sessions.all()
#         ),
#     })

# def export_project(request, project_id):
#     """Export project as JSON"""
#     project = get_object_or_404(ContentProject, id=project_id)
    
#     # Build the export structure
#     data = {
#         'project': {
#             'name': project.name,
#             'description': project.description,
#             'created_at': project.created_at.isoformat(),
#         },
#         'topics': []
#     }
    
#     for topic in project.topics.all():
#         topic_data = {
#             'title': topic.title,
#             'description': topic.description,
#             'sessions': []
#         }
        
#         for session in topic.sessions.all():
#             session_data = {
#                 'title': session.title,
#                 'description': session.description,
#                 'episodes': []
#             }
            
#             for episode in session.episodes.all():
#                 episode_data = {
#                     'title': episode.title,
#                     'description': episode.description,
#                     'script': episode.script,
#                     'duration_minutes': episode.duration_minutes,
#                 }
#                 session_data['episodes'].append(episode_data)
            
#             topic_data['sessions'].append(session_data)
        
#         data['topics'].append(topic_data)
    
#     response = JsonResponse(data, json_dumps_params={'indent': 2})
#     response['Content-Disposition'] = f'attachment; filename="project_{project.id}_export.json"'
    
#     return response

# from .services import extract_text_from_file, generate_structure_from_text

# def create_project(request):
#     if request.method == 'POST':
#         form = ContentProjectForm(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save(commit=False)

#             uploaded_file = request.FILES.get('pdf_file')
#             if uploaded_file:
#                 raw_text = extract_text_from_file(uploaded_file)
#                 project.raw_text = raw_text

#             project.save()

#             # 🧠 Generate topic/session/episode structure
#             generate_structure_from_text(project)

#             messages.success(request, f'Project "{project.name}" created and processed successfully!')
#             return redirect('project_detail', project_id=project.id)
#     else:
#         form = ContentProjectForm()

#     return render(request, 'LLM/create_project.html', {'form': form})

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



########## youtube video transcript ##########
import os
import textwrap
import requests
import yt_dlp
import webvtt
from fpdf import FPDF
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

# Utilities
def download_captions(youtube_url, lang='en'):
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'skip_download': True,
        'outtmpl': f'captions4.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def convert_vtt_to_text(lang='en'):
    vtt_file = f'captions4.{lang}.vtt'
    srt_lines = []
    text_content = []

    for i, caption in enumerate(webvtt.read(vtt_file), 1):
        srt_lines.append(f"{i}")
        srt_lines.append(f"{caption.start.replace('.', ',')} --> {caption.end.replace('.', ',')}")
        srt_lines.append(caption.text)
        srt_lines.append("")
        text_content.append(caption.text)

    full_text = " ".join(text_content)
    return full_text

def send_to_groq(text, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    chunks = textwrap.wrap(text, width=3000, break_long_words=False, break_on_hyphens=False)
    combined_output = ""

    for i, chunk in enumerate(chunks):
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a transcript formatter. Your job is to ONLY format and structure the provided YouTube transcript text..."
                },
                {
                    "role": "user",
                    "content": f"Format this transcript:\n\n{chunk}"
                }
            ],
            "temperature": 0.1
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            combined_output += f"{content}\n\n"
        except Exception as e:
            combined_output += f"{chunk}\n\n"

    return combined_output

def convert_to_pdf(text, filename="structured_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        try:
            pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
        except:
            pdf.multi_cell(0, 10, line.encode('ascii', 'ignore').decode('ascii'))

    pdf.output(filename)
    return filename

# -------------------------------
# 🎯 Django ViewVfrom django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponse
import os

@csrf_exempt
def youtube_to_pdf_view(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body.decode("utf-8"))
            youtube_url = data.get("youtube_url")

            if not youtube_url:
                return JsonResponse({"error": "YouTube URL is required."}, status=400)

            print(f"🎥 Processing YouTube URL: {youtube_url}")
            groq_api_key = "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"

            # Run the pipeline
            download_captions(youtube_url)
            raw_text = convert_vtt_to_text()
            formatted_text = send_to_groq(raw_text, groq_api_key)
            pdf_path = convert_to_pdf(formatted_text)

            # Return PDF file as a downloadable response
            return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename='formatted_transcript.pdf')

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Use POST with JSON {'youtube_url': '...'}"}, status=200)

########################################