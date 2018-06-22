import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_filename_ext(filepath):
    """
    Return file name and extension.
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def get_picture_filename(instance, filename):
    """
    Create path for the profile picture.
    """
    new_filename = instance.user.username
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile_pictures/{final_filename}".format(final_filename=final_filename)


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    picture = models.ImageField(upload_to=get_picture_filename,
                                verbose_name=_('Upload a picture'),
                                blank=True,
                                null=True)

    location = models.CharField(_('Location'), max_length=30, blank=True)
    # Regex for Pakistani Phone Number
    phone_regex = RegexValidator(regex=r'^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$',
                                 message="Invalid phone number. Please provide valid phone number.")
    phone_number = models.CharField(_('Phone Number'), validators=[phone_regex], max_length=16, blank=True)

    phone_number_verified = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    member_since = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('-member_since', )

    def __str__(self):
        return self.user.username

    def screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:  # noqa: E722
            return self.user.username

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/ditto.jpg'
        if self.picture:
            return self.picture.url
        else:
            return default_picture

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
