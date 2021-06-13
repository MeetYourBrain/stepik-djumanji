"""stepik_djumanji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vacancies.views import MainView, VacancyView, CompanyView, ListVacanciesView, VacanciesBySpecialtyView, \
    LetStartView, CreateCompanyView, MyCompanyView, MyVacanciesView, CreateVacancyView, MyVacancyDetailView, SearchView
from accounts.views import login_view, register_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls, name='admin_panel'),
    path('', MainView.as_view(), name='main'),
    path('vacancies/', ListVacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<specialty>/', VacanciesBySpecialtyView.as_view(), name='specialisation'),
    path('companies/<int:pk>/', CompanyView.as_view(), name='company'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/send/', VacancyView.as_view(), name='vacancy_send'),
    path('mycompany/letsstart/', LetStartView.as_view(), name='letsstart'),
    path('mycompany/create/', CreateCompanyView.as_view(), name='create_company'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/vacancies/', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/create/', CreateVacancyView.as_view(), name='create_vacancy'),
    path('mycompany/vacancies/<pk>', MyVacancyDetailView.as_view(), name='my_vacancy'),
    path('search/', SearchView.as_view(), name='search'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
