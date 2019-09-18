import os
import pycurl
import uuid

from django.utils import dateformat, timezone
from django.shortcuts import render
from django.views import generic
from django.db import transaction
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect

from . import forms
from . import models


class ImgsMixin(object):
    def get_context_data(self, **kwargs):
        kwargs['imgs'] = self.request.session.get('imgs', [])

        return super().get_context_data(**kwargs)


class DownloadRemote(ImgsMixin, generic.FormView):
    form_class = forms.ImageForm
    template_name = 'index.html'
    success_url = reverse_lazy('xremote:download')

    def download(self, url):
        try:
            c = pycurl.Curl()

            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.TIMEOUT, 10)
            
            response = c.perform_rb()

            c.close()
        except pycurl.error:
            response = b''

        return response

    def generate_path(self):
        path = os.path.join(settings.MEDIA_ROOT, dateformat.format(timezone.now(), 'Y/m/d'))

        if not os.path.exists(path):
            os.makedirs(path, 0o755)
        return os.path.join(path, str(uuid.uuid4()))

    @transaction.atomic
    def form_valid(self, form):
        url = form.cleaned_data['url']
        response = self.download(url)
        path = self.generate_path()

        if response:
            with open(path, 'wb') as f:
                f.write(response)

            url = path[len(settings.MEDIA_ROOT)+1:]
            models.Image.objects.create(path=url)
            if 'imgs' not in self.request.session:
                self.request.session['imgs'] = []
            self.request.session['imgs'].append(url)

            self.request.session.modified = True

        return HttpResponseRedirect(self.get_success_url())
