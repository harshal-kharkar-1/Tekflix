from django.urls import path

from . import views


urlpatterns = [
    path("api/upload", views.index, name="index"),
    # path("upload-pdf",views.upload_pdf_view, name="upload_pdf"),
    path("upload-pdf-new/", views.upload_pdf_view, name="upload_pdf"),
]



    