from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import AllProject


def filter_projects(incoming):
    if incoming.user.is_authenticated:
        try:
            location = incoming.GET['location']
            projects = AllProject.objects.filter(location__location__contains=location)
            if projects:
                return render(incoming, 'new/filter_projects.html', {'projects': projects})
            else:
                messages.error(incoming, 'Projects Not Found!')
                return HttpResponseRedirect('/project_categories/')
        except Exception as p:
            print(str(p))
            messages.error(incoming, 'Projects Not Found!')
            return HttpResponseRedirect('/project_categories/')
    else:
        return HttpResponseRedirect('/')
