from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UploadImageForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .opencv_dface import opencv_dface


def first_view(request):
  return render(request, 'opencv_webapp/first_view.html', {})

def uimage(request):
  form = UploadImageForm(request.POST, request.FILES)
  if form.is_valid():
      myfile = request.FILES['image']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      return render(request, 'opencv_webapp/uimage.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
  else:
      form = UploadImageForm()
      return render(request, 'opencv_webapp/uimage.html', {'form': form})

def dface(request):
  form = ImageUploadForm(request.POST, request.FILES)
  if request.method == 'POST':
     if form.is_valid():
        post = form.save(commit=False)
        post.save()
 
        imageURL = settings.MEDIA_URL + form.instance.document.name
        opencv_dface(settings.MEDIA_ROOT_URL + imageURL)
 
        return render(request, 'opencv_webapp/dface.html', {'form':form, 'post':post})
  else:
     form = ImageUploadForm()
  return render(request, 'opencv_webapp/dface.html',{'form':form})