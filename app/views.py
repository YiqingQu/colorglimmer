import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from colorglimmer import settings


class AccessibilityReportView(View):

    def get(self, request, *args, **kwargs):
        image_url = settings.MEDIA_URL + "DSCF0572.JPG"
        data = {
            'color_assessment': "Contains confusing colors",
            'detailed_feedback': "Problematic areas in content",
            'modification_suggestions': "Suggestions to enhance content's accessibility",
            'image_url': image_url,  # Add the image URL to the context

        }
        return render(request, 'accessibility_report.html', context=data)

    def post(self, request, *args, **kwargs):
        # Process the content sent by the user here
        data = {
            'color_assessment': "Contains confusing colors",
            'detailed_feedback': "Problematic areas in content",
            'modification_suggestions': "Suggestions to enhance content's accessibility"
        }
        return JsonResponse(data)


class ImageRecoloringView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'image_recoloring.html')

    def post(self, request, *args, **kwargs):
        # Process the image sent by the user here
        data = {
            'status': 'success',
            'message': 'Image recolored successfully!'
        }
        return JsonResponse(data)


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        # Process the uploaded file here (image or PDF)
        # For now, we just return the same page
        return render(request, 'index.html')


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
        else:
            return JsonResponse({'error': 'file not in FILES'}, status=400)

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # saves to the 'files' directory under MEDIA_ROOT
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)  # You can get the file URL if needed

    return redirect(request.META.get('HTTP_REFERER'))


class AboutUsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'about_us.html')


class ContactUsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'contact_us.html')
