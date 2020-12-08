from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'ptype', 'published')
    list_editable = ('published',)
    list_filter = ['published', 'ptype']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'done')
    list_filter = ('done',)
    list_editable = ('done',)


admin.site.register(StaticSiteData)
admin.site.register(Message)
