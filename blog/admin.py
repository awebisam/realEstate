from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Blog
# Register your models here.


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    list_display = ('title', 'published',)
    list_editable = ('published',)
    summernote_fields = ('body',)
    list_filter = ('published', )
