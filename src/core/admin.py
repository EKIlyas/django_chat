from django.contrib import admin

from core.models import Student, Manager, Subject


admin.site.register(Manager)
admin.site.register(Student)


@admin.register(Subject)
class SetAdmin(admin.ModelAdmin):
    fields = ['name']
