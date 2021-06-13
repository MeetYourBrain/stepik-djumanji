from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from vacancies.models import Company, Specialty, Vacancy, Application
from .forms import ApplicationForm, CompanyCreateForm, VacancyCreateForm


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count_vacancies=Count('vacancies'))
        context['companies'] = Company.objects.annotate(count_vacancies=Count('vacancies'))

        return context


class CompanyView(View):
    def get(self, request, pk):
        companies = Company.objects.get(id=pk)
        vacancies_in_company = Vacancy.objects.filter(company__id=pk)

        return render(request, 'company.html', context={
            'companies': companies,
            'vacancies': vacancies_in_company,
        })


class VacancyView(View):

    def get(self, request, pk):
        vacancy = get_object_or_404(Vacancy, id=pk)

        return render(request, 'vacancy.html', context={
            'vacancy': vacancy,
            'form': ApplicationForm,
            'pk': pk,
        })

    def post(self, request, pk):
        vacancy = get_object_or_404(Vacancy, id=pk)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            written_username = form.cleaned_data.get('written_username')
            written_phone = form.cleaned_data.get('written_phone')
            written_cover_letter = form.cleaned_data.get('written_cover_letter')
            if request.user.id:
                Application.objects.create(
                    written_username=written_username,
                    written_phone=written_phone,
                    written_cover_letter=written_cover_letter,
                    user=request.user,
                    vacancy=Vacancy.objects.get(id=pk),
                )
            else:
                return redirect('login')
            return render(request, 'sent.html', {'pk': pk})
        return render(request, 'vacancy.html', context={'form': form, 'pk': pk})


class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies.html'
    queryset = model.objects.select_related('specialty', 'company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = 'Все вакансии'

        return context


class VacanciesBySpecialtyView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies.html'

    def get_queryset(self):
        return (
            self.model.objects
            .filter(specialty__code=self.kwargs['specialty'])
            .select_related('specialty', 'company')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = self.kwargs['specialty']

        return context


class LetStartView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'accounts/letstart.html')


class CreateCompanyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user.id
        try:
            company = Company.objects.get(owner=user)
        except Company.DoesNotExist:
            return render(request, 'accounts/company-create.html', {'form': CompanyCreateForm})
        if user == company.owner.id:
            return redirect('my_company')

    def post(self, request):
        user = request.user
        company_create_form = CompanyCreateForm(request.POST, request.FILES)
        if company_create_form.is_valid():
            form = company_create_form.save(commit=False)
            form.owner = user
            form.save()
            messages.success(request, 'Компания создана')
            return redirect('my_company')
        else:
            return redirect('create_company')


class MyCompanyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        owner = request.user.id
        try:
            company_owner = Company.objects.get(owner_id=owner)
        except Company.DoesNotExist:
            return redirect('letsstart')
        company_update_form = CompanyCreateForm(instance=company_owner)
        return render(request, 'accounts/company-create.html', {'form': company_update_form})

    def post(self, request):
        owner = request.user.id
        company = Company.objects.get(owner_id=owner)
        company_update_form = CompanyCreateForm(request.POST, request.FILES, instance=company)
        if company_update_form.is_valid():
            company = company_update_form.save(commit=False)
            company.owner = get_object_or_404(User, id=owner)
            company.save()
            messages.success(request, 'Компания успешно изменена')
            return redirect('my_company')
        else:
            return render(request, 'accounts/company-create.html', {'form': company_update_form})


class MyVacanciesView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        try:
            company = Company.objects.get(owner_id=request.user.id)
        except Company.DoesNotExist:
            return redirect('letsstart')
        vacancies = Vacancy.objects.filter(company__id=company.id).annotate(count_app=Count('applications'))

        return render(request, 'accounts/vacancy-list.html', {'vacancies': vacancies, 'company': company.id})


class CreateVacancyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        try:
            company = Company.objects.get(owner_id=request.user.id)
        except Company.DoesNotExist:
            return redirect('letsstart')
        vacancy_create_form = VacancyCreateForm()
        response_show = False
        return render(request, 'accounts/vacancy-edit.html', {'form': vacancy_create_form,
                                                              'response_show': response_show})

    def post(self, request):
        company = Company.objects.get(owner_id=request.user.id)
        vacancy_create_form = VacancyCreateForm(request.POST)
        if vacancy_create_form.is_valid():
            form = vacancy_create_form.save(commit=False)
            form.company = company
            form.save()
            messages.success(request, 'Вакансия создана')
            return redirect('my_vacancies')
        else:
            messages.error(request, 'Вакансия не создана')
            return redirect('create_vacancy')


class MyVacancyDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        try:
            company = Company.objects.get(owner_id=request.user.id)
        except Company.DoesNotExist:
            return redirect('letsstart')
        vacancy = get_object_or_404(Vacancy, id=pk)
        responses = Application.objects.filter(vacancy_id=vacancy)
        vacancy_update_form = VacancyCreateForm(instance=vacancy)
        response_show = True
        return render(request, 'accounts/vacancy-edit.html', {'form': vacancy_update_form, 'responses': responses,
                                                              'response_show': response_show})

    def post(self, request, pk):
        company = Company.objects.get(owner_id=request.user.id)
        vacancy = get_object_or_404(Vacancy, id=pk)
        vacancy_update_form = VacancyCreateForm(request.POST, instance=vacancy)
        if vacancy_update_form.is_valid():
            vacancy = vacancy_update_form.save(commit=False)
            vacancy.company = company
            vacancy.save()
            messages.success(request, 'Вакансия успешно изменена')
            return redirect('my_vacancy', pk)
        else:
            messages.error(request, 'Вакансия не изменена')

        return render(request, 'accounts/vacancy-create.html', {'form': vacancy_update_form})

# Поиск


class SearchView(ListView):
    model = Vacancy
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        vacancy_list = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(skills__icontains=query),
        )
        return vacancy_list
