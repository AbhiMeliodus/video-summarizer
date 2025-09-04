from django.urls import path
from . import views

urlpatterns = [
    path("", views.summarize_view, name="summarize"),
    path("download/<str:filename>/", views.download_file, name="download_file"),
    path("cleanup/", views.cleanup_session_files, name="cleanup"),
]