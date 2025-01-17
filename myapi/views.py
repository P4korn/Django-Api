
from django.http import JsonResponse
from .models import *

def hello_world_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Hello, World!'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        # Optional: Validate the file type
        if not uploaded_image.name.endswith(('jpg', 'jpeg', 'png')):
            return JsonResponse({'error': 'File type not supported'}, status=400)
        
        # Save the file
        try:
            image_instance = Image(image=uploaded_image)
            image_instance.save()
            return JsonResponse({'message': 'Image uploaded successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)