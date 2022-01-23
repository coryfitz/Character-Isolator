from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from .forms import FilterForm
from django.contrib.staticfiles.storage import staticfiles_storage

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
            form.save()
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
        txtfile = request.FILES['txt_file']
        def char_isolate():

            #Open and read the uploaded file
            ur_text = txtfile.read().decode("utf-8")
            text = []
            for char in ur_text:
                if char not in text:
                    text.append(char)
            text = str(text)

            #Find unique characters
            unique = []
            for char in text:
                if char not in unique:
                    unique.append(char)
            unique = str(unique)

            #Remove punctuation and whitespace
            import string
            nopunct_unique = unique.translate(str.maketrans('', '', string.punctuation))
            nodigit_unique = nopunct_unique.translate(str.maketrans('', '', string.digits))
            noletter_unique = nodigit_unique.translate(str.maketrans('', '', string.ascii_letters))
            nochinesepunct_unique = noletter_unique.translate({ord(c): None for c in '。；：！？，、'})
            clean_unique = nochinesepunct_unique.translate({ord(c): None for c in string.whitespace})

            #Determine the filter
            preference = request.session.get('preference')

            if preference == 'NO':
                file_path = staticfiles_storage.open('converter/filternone.csv')

            elif preference == 'F250':
                file_path = staticfiles_storage.open('converter/filter250.csv')

            elif preference == 'F500':
                file_path = staticfiles_storage.open('converter/filter500.csv')

            elif preference == 'F750':
                file_path = staticfiles_storage.open('converter/filter750.csv')

            else:
                file_path = staticfiles_storage.open('converter/filter1000.csv')

            filter_file = file_path.read().decode("utf-8")

            filter = set([])
            for word in filter_file:
                filter.add(word)

            #Filter out common characters
            filtered = set([])
            for word in clean_unique:
                if word not in filter:
                    filtered.add(word)
            request.session['filtered_instance'] = list(filtered)

        char_isolate()
        success = 1
        return render(request, 'converter/file_download.html')
    context = {}
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
    path = "mysite/staticfiles/converter/sample.txt"
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
