from django import forms
from .models import Application, Company, Vacancy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']
        widgets = {
            'written_username': forms.TextInput(attrs={'class': 'form-control'}),
            'written_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'written_cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']
        widgets = {
            'logo': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn btn-info'))


class VacancyCreateForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn btn-info'))
