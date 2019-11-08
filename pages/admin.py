from django.contrib import admin

from .forms import HtmlContentForm
from .models import HtmlContent

class HtmlContentAdmin(admin.ModelAdmin):
    # this is class replacing the form to WYSIWYG one
    form = HtmlContentForm

    list_display = ('keyword', 'content_cut')

    def content_cut(self, obj):
        content = obj.content
        chars_max = 150
        if len(content) < chars_max:
            return content
        else:
            return content[:chars_max-3] + "..."


admin.site.register(HtmlContent, HtmlContentAdmin)
