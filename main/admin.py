from django.contrib import admin
from .models import File,SamDUkf
# Register your models here.

# admin.site.register(Question


@admin.register(SamDUkf)
class SamDUkfAdmin(admin.ModelAdmin):
    list_display = ('academic_year',)


admin.site.register(File)