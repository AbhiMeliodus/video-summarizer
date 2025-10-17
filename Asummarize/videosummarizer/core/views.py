from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
import os
from .services.pipeline import run_pipeline


def summarize_view(request):
    if request.method == "POST":
        youtube_url = request.POST.get("youtube_url", "").strip()
        if not youtube_url:
            return render(request, "core/index.html", {"error": "Please enter a valid YouTube URL."})

        try:
            # ✅ Correct order: pipeline returns (transcript_path, summary_path)
            transcript_path, summary_path = run_pipeline(youtube_url)

            # Store file paths in session for cleanup later
            request.session["generated_files"] = [transcript_path, summary_path]

            # Read contents of transcript and summary
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript_text = f.read()
            with open(summary_path, "r", encoding="utf-8") as f:
                summary_text = f.read()

            return render(request, "core/results.html", {
                "youtube_url": youtube_url,
                "transcript": transcript_text,
                "summary": summary_text,
                "transcript_file": os.path.basename(transcript_path),
                "summary_file": os.path.basename(summary_path),
            })

        except Exception as e:
            return render(request, "core/index.html", {"error": f"Error: {e}"})

    return render(request, "core/index.html")


def download_file(request, filename):
    """Serve transcript or summary file for download"""
    # ✅ Ensure absolute path using BASE_DIR
    download_dir = os.path.join(settings.BASE_DIR, "downloads")
    file_path = os.path.join(download_dir, filename)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    # ✅ Return file with Content-Disposition header
    response = FileResponse(open(file_path, "rb"), as_attachment=True)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def cleanup_session_files(request):
    """Delete generated files when session ends"""
    files = request.session.get("generated_files", [])
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)
    request.session.pop("generated_files", None)
    return HttpResponse("✅ Cleanup complete.")