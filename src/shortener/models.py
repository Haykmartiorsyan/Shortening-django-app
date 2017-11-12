from django.db import models
from .utils import code_generator, create_shortcode
from django.conf import settings
from .validators import validate_url, validate_dot_com
from django.core.urlresolvers import reverse



SHORTCODE_MAX_LENGHT = getattr(settings, 'SHORTCODE_MAX_LENGHT', 15)


class KirrUrlManager(models.Model):
    def all(self, *args, **kwargs):
        qs_main = super(KirrUrlManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = KirrUrl.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_codes += 1
            return 'New codes made: {i}'.format(i=new_codes)


class KirrUrl(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(max_length=SHORTCODE_MAX_LENGHT, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestap = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = KirrUrlManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        super(KirrUrl, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse('scode', kwargs={'shortcode': self.shortcode})
        return 'http://127.0.0.1:8000' + url_path