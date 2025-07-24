from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")




from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
import tempfile, shutil, os
import logging
from .pdf_processor import load_pdf, extract_hierarchical_topics, convert_to_separate_topic_dicts


logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def upload_pdf_view(request):
    if request.method == "GET":
        return render(request, "welcome.html")  # Render form on GET

    try:
        if 'file' not in request.FILES:
            return HttpResponseBadRequest("Missing PDF file in request.")

        uploaded_file = request.FILES['file']
        if not uploaded_file.name.lower().endswith('.pdf'):
            return HttpResponseBadRequest("Only PDF files are supported.")

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            shutil.copyfileobj(uploaded_file.file, tmp_file)
            tmp_file_path = tmp_file.name

        text = load_pdf(tmp_file_path)
        if not text.strip():
            return JsonResponse({"error": "No text found in PDF"}, status=400)

        result = extract_hierarchical_topics(text)
        nested_structure = convert_to_separate_topic_dicts(result)

        response_data = {
            "success": True,
            "filename": uploaded_file.name,
            "document_summary": result.document_summary,
            "topics": [topic.dict() for topic in result.topics],
            "nested_structure": nested_structure,
            "stats": {
                "total_topics": len(result.topics),
                "total_sessions": sum(len(topic.sessions) for topic in result.topics),
                "total_episodes": sum(len(session.episodes) for topic in result.topics for session in topic.sessions)
            }
        }
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        logger.exception("Error processing PDF:")
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
