import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.staticfiles.storage import staticfiles_storage
from .forms import FilterForm
from .converter_utils import get_unique_characters, filter_characters

def index(request):
    return render(request, "converter/index.html")

def about(request):
    return render(request, "converter/about.html")

def filter(request):
    if request.method != 'POST':
        #No data submitted; create a blank form
        form = FilterForm()
    else:
        #POST data submitted; process data
        form = FilterForm(data=request.POST)
        if form.is_valid():
            preference = form.cleaned_data['preference']
            request.session['preference'] = preference
            #form.save()
            return HttpResponseRedirect('file_upload')
        else:
            context = {'form':form}
            return render(request, "converter/index.html", context)
    context = {'form':form}
    return render(request, "converter/filter.html", context)

def file_upload(request):
    success = 0
    if success == 1:
        success = 2
    if request.POST and request.FILES:

        # read the file and get only the unique characters
        txtfile = request.FILES['txt_file']
        ur_text = txtfile.read().decode("utf-8")
        unique = get_unique_characters(ur_text)

        # filter out the most common characters based on user preference
        preference = request.session.get('preference')
        filtered = filter_characters(unique, preference)
        request.session['filtered_instance'] = list(filtered)
        
        success = 1
        return render(request, 'converter/file_download.html')
    return render(request, "converter/file_upload.html", locals())

def download(request):
    #Write to file
    filtered = request.session.get('filtered_instance')
    tmp_path = os.path.join(settings.MEDIA_ROOT, 'tmp/text.txt')
    with open(tmp_path, 'w') as f:
        item = iter(filtered)
        for _ in range(len(filtered)-1):
            f.write('%s\n' % next(item))
        f.seek(0)
        f.write('%s' % next(item))
    f.close()

    path = "tmp/text.txt"
    new_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(new_path):
        with open(new_path, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(new_path)
                return response
            except Exception:
                raise Http404

def sample(request):
    path = "staticfiles/converter/sample.txt"
    new_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(new_path):
        with open(new_path, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(new_path)
                return response
            except Exception:
                raise Http404

def feedback(request):
    return render(request, "converter/feedback.html")