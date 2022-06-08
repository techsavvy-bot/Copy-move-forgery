from django.shortcuts import render
from tempo.detection import twoImageForgery

from tempo.models import Articles
from .forms import twoImage, uploadForm
from tempo.forgery_detection import forgery
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.contrib.auth import authenticate, login, logout
from myapp.settings import BASE_DIR
from django.contrib.auth.decorators import login_required

# Create your views here.


# def home(request):
#     # forgery()

#     return render(request, 'index.html')
@login_required(login_url='/login')
def image(request):
    return render(request, 'imgShow.html')

@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        # print("yes")
        # image = request.POST.get('formFile')
        # print(type(image))
        form = uploadForm(request.POST, request.FILES)
        # print(form)
        # print(form.is_valid())
        if form.is_valid():
            data = request.FILES['img']
            article = request.POST['article']
            if os.path.exists(f'{BASE_DIR}/media/temp.png'):
                print("Inside")
                os.remove(f'{BASE_DIR}/media/temp.png')
            path = default_storage.save(
                f'{BASE_DIR}/media/temp.png', ContentFile(data.read()))
            print(path)
            # print(str(data))
            # print("forgery status: ",forgery())
            status = forgery()
            if status:
                return redirect('/image')
            else:
                object = Articles.objects.create(image=data, article=article)
                object.save()
                return redirect('/')
    else:
        form = uploadForm()
    return render(request, 'upload.html', {'form': form})

def twoImageUpload(request):
    if request.method=='POST':
        data1 = request.FILES['image1']
        data2 = request.FILES['image2']
        if os.path.exists(f'{BASE_DIR}/media/image1.png'):
            # print("Inside")
            os.remove(f'{BASE_DIR}/media/image1.png')
        if os.path.exists(f'{BASE_DIR}/media/image2.png'):
            # print("Inside")
            os.remove(f'{BASE_DIR}/media/image2.png')
        path1 = default_storage.save(f'{BASE_DIR}/media/image1.png', ContentFile(data1.read()))
        path2 = default_storage.save(f'{BASE_DIR}/media/image2.png', ContentFile(data2.read()))
        status  = twoImageForgery()
        print("Status: ",status)
        return redirect('/result')
    else:
        form=twoImage()
    return render(request,'upload2.html',{'form':form})

def result(request):
    return render(request,'twoImgShow.html')

@login_required(login_url='/login')
def articlesPage(request):
    data = Articles.objects.all()
    return render(request, 'articles.html', {'data': data})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html")
    context = {}

    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('/login')

def signup(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, "signup.html", context)


    