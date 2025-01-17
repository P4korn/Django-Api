
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image  # Ensure the model exists
import os

@csrf_exempt
def hello_world_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Hello, World!'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Validate the file type securely
        valid_extensions = ['jpg', 'jpeg', 'png']
        file_extension = os.path.splitext(uploaded_image.name)[-1].lower().strip('.')
        if file_extension not in valid_extensions:
            return JsonResponse({'error': 'File type not supported'}, status=400)

        # Save the file
        try:
            image_instance = Image(image=uploaded_image)
            image_instance.save()
            return JsonResponse({'message': 'Image uploaded successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error saving image: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)