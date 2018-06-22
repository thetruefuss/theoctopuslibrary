from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField


@python_2_unicode_compatible
class Book(models.Model):

    CATEGORY_CHOICES = (
        ('000', _('Computer science, information and general works')),
        ('100', _('Philosophy and psychology')),
        ('200', _('Religion')),
        ('300', _('Social Sciences')),
        ('400', _('Language')),
        ('500', _('Science')),
        ('600', _('Technology and applied science')),
        ('700', _('Arts and recreation')),
        ('800', _('Literature')),
        ('900', _('History and geography')),
    )

    title = models.CharField(_('Book Title'), max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(_('Description'), max_length=5000, blank=True, null=True)
    category = models.CharField(_('Select Category'), max_length=3, choices=CATEGORY_CHOICES, default='000')
    is_free = models.BooleanField(_('Check to give away your book for free.'), default=True)
    price = models.IntegerField(_('Add a price'), default=0, blank=True)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=25, blank=True)

    submitter = models.ForeignKey(User, related_name='posted_books', on_delete=models.CASCADE)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.location = self.submitter.profile.location
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_detail',
                       args=[self.slug])


def get_photo_filename(instance, filename):
    title = instance.book.title
    slug = slugify(title)
    return "book_photos/%s-%s" % (slug, filename)


@python_2_unicode_compatible
class Photo(models.Model):

    book = models.ForeignKey(Book, default=None, related_name='book_photos', on_delete=models.CASCADE)
    photo = models.ImageField(_('Upload photos'), upload_to=get_photo_filename)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
        ordering = ('-created', )

    def __str__(self):
        return self.photo.name
