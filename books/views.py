from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from mysite.decorators import ajax_required

from .forms import BookForm, PhotoForm
from .models import Book, Photo
from .utils import check_details_status


def homepage(request):
    """
    View the homepage with search box.
    """
    show_search_box = True
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY

    return render(request, 'books/homepage.html', {
        'show_search_box': show_search_box,
        'GOOGLE_API_KEY': GOOGLE_API_KEY,
    })


def book_detail(request, book_slug):
    """
    View the book details with all photos.
    """
    book = get_object_or_404(Book, slug=book_slug)
    book_photos = book.book_photos.all()

    show_search_box = True
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY

    return render(request, 'books/book_detail.html', {
        'book': book,
        'book_photos': book_photos,
        'show_search_box': show_search_box,
        'GOOGLE_API_KEY': GOOGLE_API_KEY,
    })


@login_required
def book_post(request):
    """
    View the submit page or post a new book with/without photos.
    """
    user = request.user

    if check_details_status(user):
        PhotoFormSet = modelformset_factory(Photo,
                                            form=PhotoForm,
                                            extra=3)
        if request.method == 'POST':
            bookForm = BookForm(request.POST)
            formset = PhotoFormSet(request.POST, request.FILES,
                                   queryset=Photo.objects.none())

            if bookForm.is_valid() and formset.is_valid():
                book_form = bookForm.save(commit=False)
                book_form.submitter = request.user
                book_form.save()

                for form in formset.cleaned_data:
                    photo = form.get('photo', '')
                    if photo != '':
                        photo = Photo(book=book_form, photo=photo)
                        photo.save()

                return redirect("/")
            else:
                print(bookForm.errors, formset.errors)
        else:
            bookForm = BookForm()
            formset = PhotoFormSet(queryset=Photo.objects.none())

        return render(request, 'books/book_post_form.html', {
            'bookForm': bookForm,
            'formset': formset,
        })
    else:
        messages.info(request, 'To submit a book, you need to provide your contact details.')
        return redirect('settings')


def search_results(request):
    """
    View that handle GET search by book title, location or category.
    """
    search_query = request.GET.get('search_query', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')

    if search_query or location or category:
        all_results = Book.objects.filter(
            title__icontains=search_query,
            location__icontains=location,
            category__icontains=category
        )

        paginator = Paginator(all_results, 10)
        page = request.GET.get('page')
        if paginator.num_pages > 1:
            p = True
        else:
            p = False
        try:
            results = paginator.page(page)

        except PageNotAnInteger:
            results = paginator.page(1)

        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        page_obj = results

        show_search_box = True
        GOOGLE_API_KEY = settings.GOOGLE_API_KEY

        return render(request, 'books/search_results.html', {
            'results': results,
            'show_search_box': show_search_box,
            'GOOGLE_API_KEY': GOOGLE_API_KEY,
            'p': p,
            'page': page,
            'page_obj': page_obj
        })
    else:
        return redirect('homepage')


@ajax_required
def contact_details(request, book_id):
    """
    View the contact details of the book submitter.
    """
    data = dict()
    book = get_object_or_404(Book, id=book_id)

    user = book.submitter
    context = {'user': user}
    html_data = render_to_string(
        'books/partial_contact_box.html',
        context,
        request=request,
    )

    data['html_data'] = html_data
    return JsonResponse(data)


@login_required
@ajax_required
def activate_book(request, book_id):
    """
    View that let book submitters to activate their books.
    """
    data = dict()
    book = get_object_or_404(Book, id=book_id)

    if request.user == book.submitter:
        book.is_active = True
        book.save()
        data['is_activated'] = True
    else:
        data['is_activated'] = False

    return JsonResponse(data)


@login_required
@ajax_required
def deactivate_book(request, book_id):
    """
    View that let book submitters to deactivate their books.
    """
    data = dict()
    book = get_object_or_404(Book, id=book_id)

    if request.user == book.submitter:
        book.is_active = False
        book.save()
        data['is_deactivated'] = True
    else:
        data['is_deactivated'] = False

    return JsonResponse(data)
