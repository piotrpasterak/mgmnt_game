from django import forms
from django.db import models

from redactor.widgets import AdminRedactorEditor

from .models import HtmlContent

class RedactorEditorWidget(AdminRedactorEditor):
    # this is only updating RedactorEditor for django 2.2+
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs=attrs)

class MetaHtmlContentForm(type):
    # this is metaclass for the form
    model = HtmlContent
    fields = ('keyword', 'content',)

class HtmlContentForm(forms.ModelForm):
    # this is form creator class
    content = forms.CharField(widget=RedactorEditorWidget)
    __metaclass__ = MetaHtmlContentForm
