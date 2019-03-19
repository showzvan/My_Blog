from django.contrib import admin
from .models import ReadNum


@admin.register(ReadNum)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_object')
