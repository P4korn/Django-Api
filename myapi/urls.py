from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello_world_view, name='hello_world'),
    path('upload-images',views.upload_image,name='upload_image'),
    path('user_login',views.user_login, name='user_login')

]
