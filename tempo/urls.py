from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    # path('', views.home, name="home"),
    path('upload', views.upload, name="upload"),
    path('result',views.result,name="result"),
    path('uploadtwo',views.twoImageUpload,name="twoImageUpload"),
    path('image', views.image, name="image"),
    path('login', views.loginPage, name="loginPage"),
    path('logout', views.logoutUser, name="logoutUser"),
    path('', views.articlesPage, name="articlesPage"),
]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
