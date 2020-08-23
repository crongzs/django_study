from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse


# ---------------- HTML + Python 普通文件上传 ----------------
class FileView1(View):

    def get(self, request):
        return render(request, 'app6/app6-1普通文件上传.html')

    def post(self, request):
        file = request.FILES.get('upFile')
        with open('/Users/ku_rong/Desktop/upFile.pdf', 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)

        return HttpResponse("ok")


from app6.models import UpFiles


class FileView2(View):

    def get(self, request):
        return render(request, 'app6/app6-1普通文件上传.html')

    def post(self, request):
        file = request.FILES.get('upFile')
        title = request.POST.get('title')
        UpFiles.objects.create(title=title, file=file)

        return HttpResponse("ok")


from app6.forms import FileForm


class FileView3(View):

    def get(self, request):
        return render(request, 'app6/app6-2models文件上传.html')

    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("successful")
        else:
            print(form.errors.get_json_data())
            return HttpResponse("fial")


from app6.forms import ImageForm


class FileView4(View):

    def get(self, request):
        return render(request, 'app6/app6-3图片上传.html')

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("successful")
        else:
            print(form.errors.get_json_data())
            return HttpResponse("fial")


from django.http import StreamingHttpResponse


class FileUploadView(View):

    def get(self, request):
        '''
        文件下载
        '''

        file = UpFiles.objects.get(title='app6-6').file
        # app6/files/多测合一0629对接沟通记录.md
        file_name = file.name[11:]
        file_path = file.path

        def file_iterator(file_path, chunk_size=512):
            with open(file_path) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format('112.doc')

        return response
