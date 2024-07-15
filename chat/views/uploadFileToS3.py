from chat_app.utils import jwt_required, upload_file_to_s3
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def uploadFileToS3(request):
    try:
        print(request.FILES)
        # Check if the request contains files
        if 'files' in request.FILES:
            # Loop through the uploaded files
            for file in request.FILES.getlist('files'):
                # Upload the file to S3 and get the URL
                file_url = upload_file_to_s3(file, file.name)
                
                # Return the uploaded file URL
                return JsonResponse({'uploadedFile': file_url})
        else:
            return JsonResponse({'error': 'No files were uploaded'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)