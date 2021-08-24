from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)  # отображение даты создание постов


admin.site.register(Todo, TodoAdmin)

# Register your models here.
