from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Project


def dashboard(incoming):
    if incoming.user.is_authenticated:

        farm_count = Project.objects.all().filter(category__contains='Farm').count()
        machine_count = Project.objects.all().filter(category__contains='Machinery').count()
        land_count = Project.objects.all().filter(category__contains='Land').count()
        apartment_count = Project.objects.all().filter(category__contains='Apartment').count()
        return render(incoming, 'dashboard.html', {'farm_count': farm_count, 'machine_count': machine_count,
                                                   'land_count': land_count, 'apartment_count': apartment_count })
    else:
        return HttpResponseRedirect('/login/')
