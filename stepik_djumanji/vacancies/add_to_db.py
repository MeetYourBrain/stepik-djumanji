import os

import django
import data

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_djumanji.settings'
django.setup()

from vacancies.models import Specialty, Company, Vacancy

if __name__ == '__main__':
    for company in data.companies:
        companies = Company.objects.create(
            name=company['title'],
            location=company['location'],
            logo=company['logo'],
            description=company['description'],
            employee_count=company['employee_count'],
        )

    for spec in data.specialties:
        speciality = Specialty.objects.create(
            code=spec['code'],
            title=spec['title'],
        )
    for job in data.jobs:
        vacancy = Vacancy.objects.create(
            title=job['title'],
            specialty=Specialty.objects.get(code=job['specialty']),
            company=Company.objects.get(id=job['company']),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )
