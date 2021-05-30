from django.shortcuts import render
from django.http import Http404
from django.db.models import Count

from vacancies.models import Company, Specialty, Vacancy


def main_view(request):
    companies = Company.objects.annotate(count_vacancies=Count('vacancies'))
    specialties = Specialty.objects.annotate(count_vacancies=Count('vacancies'))

    return render(request, 'index.html', context={
        'specialties': specialties,
        'companies': companies
        })


def vacancies_view(request):
    title = 'Все вакансии'

    return render(request, 'vacancies.html', context={
        'vacancies': Vacancy.objects.all(),
        'title': title
    })


def specialisation_view(request, vacancy_code):
    try:
        vacancies = Vacancy.objects.filter(specialty__code=vacancy_code)
        vacancies_title = Specialty.objects.filter(code=vacancy_code).first().title
    except AttributeError:
        raise Http404()

    return render(request, 'vacancies.html', context={
        'vacancies': vacancies,
        'vacancies_title': vacancies_title
    })


def company_view(request, pk):
    try:
        companies = Company.objects.get(id=pk)
        vacancies_in_company = Vacancy.objects.filter(company__id=pk)
    except Company.DoesNotExist:
        raise Http404()
    except Vacancy.DoesNotExist:
        raise Http404()

    return render(request, 'company.html', context={
        'companies': companies,
        'vacancies': vacancies_in_company
    })


def vacancy_view(request, pk):
    try:
        vacancy = Vacancy.objects.get(id=pk)
    except Vacancy.DoesNotExist:
        raise Http404()

    return render(request, 'vacancy.html', context={
        'vacancy': vacancy
    })
