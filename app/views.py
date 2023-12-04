import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from colorglimmer.utils import simulate_deuteranopia, calculate_histogram, compare_histograms, calculate_ssim, calculate_RGB, calculate_grayscale_histogram, recolor_image
from openai import OpenAI
import openai
from colorglimmer import settings
import json
import numpy as np

openai.api_key = "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"
gpt = OpenAI(api_key=openai.api_key)
messages=[{"role": "system", "content": "You are a visual effects designer to identify if an image is red and green color blind/weakness friendly"}]



class ModificationSuggestion(View):

    def get(self, request, *args, **kwargs):
        file = request.GET.get('filename', None)
        # origin_image = settings.MEDIA_URL + file
        origin_image = os.path.join(settings.MEDIA_ROOT, file)
        red, green, blue = calculate_RGB(origin_image)
        grey_histogram = calculate_grayscale_histogram(origin_image)

        data = {
            "red_channel": {
                "mean": float(np.mean(red)),
                "median": float(np.median(red)),
                "max": int(np.max(red)),
                "min": int(np.min(red)),
                "std": float(np.std(red))
            },
            "green_channel": {
                "mean": float(np.mean(green)),
                "median": float(np.median(green)),
                "max": int(np.max(green)),
                "min": int(np.min(green)),
                "std": float(np.std(green))
            },
            "grey_histogram": grey_histogram.tolist()
        }

        json_data = json.dumps(data)
        print(json_data)
        messages.append({"role": "user",
                         "content": "This is the parameter of the image you need to analyze: " + json_data + "Please take a look. "})
        messages.append({"role": "user",
                         "content": "Give me your evaluation on this image in terms of [color assessment], [detailed feedback], [modification suggestions], and [suggested_RGB_values] in a Json format data. [suggested_RGB_values] includes two fields, 'red' and 'green', whose value should be the RGB value of other random color that doesn't look even close to red and green in the format of Python's tuple of three elements without double quotation mark, to replace red and green, respectively, to be color-blindness/weakness friendly that retains some beauty, "})
        print(type(messages))
        try:
            response = gpt.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                response_format={"type": "json_object"}
                # max_tokens=300  # limit the response to 300 token to prevent it to be too long
            )
            print(response.choices[0].message.content)
            result_json = response.choices[0].message.content
        except json.JSONDecodeError:
            return 'error: Invalid JSON format'
        messages.append({"role": "assistant", "content": response})
        print(result_json)
        result_data = json.loads(result_json)
        suggested_color = result_data['suggested_RGB_values']
        modified_img, new_file = recolor_image(origin_image, file, suggested_color)
        result_data["modified_url"] = settings.MEDIA_URL + new_file

        return render(request, 'modification_suggestion.html', context=result_data)


class AccessibilityReportView(View):

    def get(self, request, *args, **kwargs):
        file = request.GET.get('filename', None)
        # origin_image = settings.MEDIA_URL + file
        origin_image = os.path.join(settings.MEDIA_ROOT, file)
        processed_image, new_file = simulate_deuteranopia(origin_image, file)

        hist1 = calculate_histogram(origin_image)
        hist2 = calculate_histogram(processed_image)
        similarity = compare_histograms(hist1, hist2)
        normalized_simi = (similarity + 1) / 2

        ssim_value = calculate_ssim(origin_image, processed_image)
        normalized_ssim_diff = (1 + ssim_value) / 2

        score = round((0.8 * normalized_simi + 0.2 * normalized_ssim_diff) * 100)
        data = {
            'color_assessment': "Contains confusing colors",
            'detailed_feedback': "Problematic areas in content",
            'modification_suggestions': "Suggestions to enhance content's accessibility",
            'origin_url': settings.MEDIA_URL + file,
            'processed_url': settings.MEDIA_URL + new_file,
            'score': score
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

class ScoreReportView(View):

    def get(self, request, *args, **kwargs):
        print(111)
        file = request.GET.get('filename', None)
        # origin_image = settings.MEDIA_URL + file
        origin_image = os.path.join(settings.MEDIA_ROOT, file)
        processed_image, new_file = simulate_deuteranopia(origin_image, file)

        hist1 = calculate_histogram(origin_image)
        hist2 = calculate_histogram(processed_image)
        similarity = compare_histograms(hist1, hist2)
        normalized_simi = (similarity + 1) / 2

        ssim_value = calculate_ssim(origin_image, processed_image)
        normalized_ssim_diff = (1 + ssim_value) / 2

        score = round((0.8 * normalized_simi + 0.2 * normalized_ssim_diff) * 100)
        data = {
            'origin_url': settings.MEDIA_URL + file,
            'processed_url': settings.MEDIA_URL + new_file,
            'score': score
        }
        return render(request, 'score.html', context=data)

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
