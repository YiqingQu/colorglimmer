from django.shortcuts import render
from django.http import JsonResponse
from django.views import View


class AccessibilityReportView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accessibility_report.html')

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


class AboutUsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'about_us.html')


class ContactUsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'contact_us.html')
