from django.shortcuts import render

from hr.models import AllProject


def get_farms(incoming):
    farms = AllProject.objects.all().filter(category__contains='Farm')
    return render(incoming, 'analysis/farms.html', {'farms': farms})
