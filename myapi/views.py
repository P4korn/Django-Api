
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import os
from django.conf import settings

@csrf_exempt
def hello_world_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Hello, World!'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Optional: Validate the file type
        if not uploaded_image.name.endswith(('jpg', 'jpeg', 'png')):
            return JsonResponse({'error': 'File type not supported'}, status=400)

        # Upload the image to S3
        try:
            # Using IAM role credentials automatically
            s3_client = boto3.client('s3')

            s3_key = 'images/' + uploaded_image.name  # You can modify the key to fit your needs

            # Upload the file to S3
            s3_client.upload_fileobj(uploaded_image, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

            # Construct the S3 URL for the uploaded image
            image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

            return JsonResponse({'message': 'Image uploaded successfully!', 'image_url': image_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error saving image: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
