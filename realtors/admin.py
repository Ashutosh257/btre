from django.contrib import admin
from .models import Realtor

class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'is_mvp', 'hire_date')
    list_editable = ('is_mvp',)

admin.site.register(Realtor, RealtorAdmin)
