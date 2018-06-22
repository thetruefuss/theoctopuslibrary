from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from mysite.decorators import ajax_required

from .forms import FeedbackForm, ReportForm


@login_required
@ajax_required
def report(request):
    """
    View that handle user reports related to books.
    """
    data = dict()

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            data['success'] = True
        else:
            data['failure'] = True
        return JsonResponse(data)
    else:
        form = ReportForm()
        context = {'form': form}
        html_data = render_to_string('core/partial_report.html',
            context,
            request=request,
        )
        data['html_data'] = html_data
        return JsonResponse(data)


def feedback(request):
    """
    View the feedback page or post a feedback.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback sent successfully.')
            return redirect('homepage')
        else:
            messages.error(request, 'An error occurred while submitting the form.')
            return redirect('homepage')
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback_form.html', {'form': form})


def terms(request):
    return render(request, 'core/terms.html', {})


def privacy(request):
    return render(request, 'core/privacy.html', {})


def about(request):
    return render(request, 'core/about.html', {})

def faq(request):
    return render(request, 'core/faq.html', {})
