from django import forms

from .models import Feedback, Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('content', )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'message', )
