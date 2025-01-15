from django.http import JsonResponse

def hello_world_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Hello, World!'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)