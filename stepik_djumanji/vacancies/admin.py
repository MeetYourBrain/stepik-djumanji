from django.contrib import admin
from .models import Vacancy, Company, Specialty, Application


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'published_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'company')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'owner')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'location', 'owner')


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code')
    list_display_links = ('id', 'title')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'written_username', 'written_phone', 'vacancy', 'user')
    list_display_links = ('id', 'written_username')
    search_fields = ('written_username', 'written_phone', 'vacancy', 'user')


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationAdmin)
