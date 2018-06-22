from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

import requests
from books.models import Book

from mysite.decorators import ajax_required

from .forms import (LocationEditForm, PhoneNumberEditForm,
                    ProfilePictureEditForm, SignUpForm, UserEditForm)
from .models import Profile
from .tokens import account_activation_token


def signup(request):
    """
    View the sign up page or create a new account.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your The Octopus Library Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@ajax_required
def validate_username(request):
    """
    View that checks username availability.
    """
    username = request.GET.get('username', None)

    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'

    return JsonResponse(data)


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    """
    View that activates the user account by validating the activation token.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # if x_forwarded_for:
    #     ip_address = x_forwarded_for.split(',')[-1].strip()
    # else:
    #     ip_address = request.META.get('REMOTE_ADDR')
    #
    # response = requests.get('http://freegeoip.net/json/%s' % ip_address)
    # geodata = response.json()

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        # Populate the user's location by using their IP address.
        # if geodata['city'] and geodata['region_name'] and geodata['country_name']:
        #     location = geodata['city'] + ', ' + geodata['region_name'] + ', ' + geodata['country_name']
        #     user.profile.location = location
        user.save()
        login(request, user)
        return redirect('homepage')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


@login_required
def user_profile(request, username):
    """
    View the user profile page.
    """
    user = get_object_or_404(User, username=username)
    active_threads = Book.objects.filter(submitter=user, is_active=True).count()
    deactive_threads = Book.objects.filter(submitter=user, is_active=False).count()
    profile = user.profile

    return render(request, 'accounts/user_profile.html', {
        'user': user,
        'profile': profile,
        'active_threads': active_threads,
        'deactive_threads': deactive_threads,
    })


@login_required
def book_threads(request, username):
    """
    View the user submitted books.
    """
    user = get_object_or_404(User, username=username)
    posted_books = user.posted_books.filter(is_active=True)

    return render(request, 'accounts/book_threads.html', {
        'user': user,
        'posted_books': posted_books,
    })


@login_required
def deactivated_book_threads(request):
    """
    View the deactivated books list.
    """
    user = request.user
    posted_books = user.posted_books.filter(is_active=False)

    return render(request, 'accounts/deactivated_book_threads.html', {
        'user': user,
        'posted_books': posted_books,
    })


@login_required
def settings(request):
    """
    View the settings page or post the form to change user/profile related info.
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        phone_number_form = PhoneNumberEditForm(instance=request.user.profile, data=request.POST)
        profile_picture_form = ProfilePictureEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)  # noqa: E501
        location_form = LocationEditForm(instance=request.user.profile, data=request.POST)

        if user_form.is_valid():
            user_form.save()
        else:
            user_form = UserEditForm(instance=request.user)

        if phone_number_form.is_valid():
            phone_number_form.save()
        else:
            phone_number_form = PhoneNumberEditForm(instance=request.user)

        if profile_picture_form.is_valid():
            profile_picture_form.save()
        else:
            profile_picture_form = ProfilePictureEditForm(instance=request.user)

        if location_form.is_valid():
            location_form.save()
        else:
            location_form = LocationEditForm(instance=request.user)

        return redirect('settings')

    else:
        user_form = UserEditForm(instance=request.user)
        phone_number_form = PhoneNumberEditForm(instance=request.user.profile)
        profile_picture_form = ProfilePictureEditForm()
        location_form = LocationEditForm(instance=request.user.profile)
        user = request.user

    return render(request, 'accounts/settings.html', {
        'user_form': user_form,
        'phone_number_form': phone_number_form,
        'profile_picture_form': profile_picture_form,
        'location_form': location_form,
        'user': user,
    })


@login_required
def delete_account(request):
    """
    View that let user delete the account.
    """
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.delete()
    return redirect('/')
