import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def hello_world_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Sawasdee!'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):

        username = request.headers.get("username")
        password = request.headers.get("password")

        try:
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'message': 'Invalid Credential'}, status=401)

            uploaded_image = request.FILES['image']

            if not uploaded_image.name.endswith(('jpg', 'jpeg', 'png')):
                return JsonResponse({'error': 'File type not supported'}, status=400)

            s3_client = boto3.client('s3')
            s3_key = f'images/{uploaded_image.name}' 

            s3_client.upload_fileobj(uploaded_image, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

            image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

            return JsonResponse({'message': 'Image uploaded successfully!', 'image_url': image_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error saving image: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            username = request.headers.get("username")
            password = request.headers.get("password")

            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "message": "Login successful",
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                }, status=200)
            else:
                return JsonResponse({'message': 'Invalid Credential'}, status=401)

        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
