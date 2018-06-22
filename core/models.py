from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from books.models import Book


class Report(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(_('Reason'), max_length=5000)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ('-created', )

    def __str__(self):
        return self.book.title


class Feedback(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=5000)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedback')
        ordering = ('-created', )

    def __str__(self):
        return self.name
