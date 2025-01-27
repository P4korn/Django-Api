
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
from django.conf import settings
from decouple import config
from ldap3 import Server, Connection, ALL
# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

# @csrf_exempt
def hello_world_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Sawasdee!'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):

        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password :
            return JsonResponse({"error": "Please insert username or password correctly"}, status=400)
        
        user = ldap_search(username=username, password=password)

        if not user :
            return JsonResponse({'message': 'Invalid Credential'}, status=401)
        
        uploaded_image = request.FILES['image']

        if not uploaded_image.name.endswith(('jpg', 'jpeg', 'png')):
            return JsonResponse({'error': 'File type not supported'}, status=400)

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


@csrf_exempt
def user_login(request):
    if request.method == 'POST':

        try:
            username = request.POST["username"] if request.POST["username"] else False
            password = request.POST["password"] if request.POST["password"] else False

            if username and password :

                print("username : " + username)
                print("password : " + password)
                # Authenticate the user against Active Directory
                user = ldap_search(username=username, password=password)

                if user:
                    # # If authentication is successful, generate JWT tokens
                    # refresh = RefreshToken.for_user(user)

                    return JsonResponse({'message': 'Login successfully!'}, status=200)
                    # Response(
                    # #     {
                    # #         "message": "Login successful",
                    # #         "refresh_token": str(refresh),
                    # #         "access_token": str(refresh.access_token),
                    # #     },
                    #     # status=status.HTTP_200_OK,
                    # )
                else :
                    return JsonResponse({'message': 'Invalid Credential'}, status=401)
                
            else :
                return JsonResponse({"error": "Please insert username or password correctly"}, status=400)    

        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
        
def ldap_search(username, password):
    try:
        # Connect to the LDAP server
        server = Server(config("LDAP_SERVER_URI"), get_info=ALL)
        conn = Connection(server, config("LDAP_BIND_DN"), config("LDAP_BIND_PASSWORD"), auto_bind=True)

        SEARCH_BASE = 'OU=groups,DC=diller,DC=com'  # Base DN for the search
        SEARCH_FILTER = f'(sAMAccountName={username})'  # LDAP filter to search for the user
        SEARCH_ATTRIBUTES = ['cn', 'sAMAccountName', 'mail', 'memberOf', 'userPassword']
        
        # Perform the search
        conn.search(
            search_base=SEARCH_BASE,
            search_filter=SEARCH_FILTER,
            attributes=SEARCH_ATTRIBUTES
        )
        
        # Print the results
        if conn.entries:
            
            entry = conn.entries[0]

            sAMAccountName = entry.sAMAccountName
            userPassword = entry.userPassword

            if username != sAMAccountName :
                return False
            
            if password != userPassword :
                return False
            
            conn.unbind()
            return True
        
        else:
            return False
        
    except Exception as e:
        print(f"An error occurred: {e}")




