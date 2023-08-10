from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        size = myfile.size
        if size > 1 * 1024 * 1024:
            return HttpResponse('File too large', status=400)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print('saved file', filename)
    return render(request, 'requestdataapp/file-upload.html')

# Create your views here.
