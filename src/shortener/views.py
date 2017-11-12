from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from .models import KirrUrl
from .forms import SubmitUrlForm
from analytics.models import ClickEvent


def home_view_fbv(request, *args, **kwargs):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'shortener/home.html', {})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            'form': the_form,
            'title': "Shortening URL"
        }
        return render(request, 'shortener/home.html', context)

    def post(self, request, *args, **kwargs):

        form = SubmitUrlForm(request.POST)
        context = {
            'form': form,
            'title': "Short URL"
        }
        template = 'shortener/home.html'
        if form.is_valid():

            new_url = form.cleaned_data.get('url')
            obj, created = KirrUrl.objects.get_or_create(url=new_url)

            context = {
                'object': obj,
                'created': created
            }
            if created:
                template = 'shortener/success.html'
            else:
                template = 'shortener/already-exist.html'

        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = KirrUrl.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        return HttpResponseRedirect(obj.url)
