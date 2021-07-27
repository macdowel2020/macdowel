import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Location


def project_categories(incoming):
    if incoming.user.is_authenticated:
        if incoming.method == 'POST' and incoming.user.is_superuser:
            try:
                location = incoming.POST['location']
                description = incoming.POST['description']

                Location.objects.create(
                    code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                    location=location,
                    description=description
                )
                messages.success(incoming, 'Location Added Successfully')
                return HttpResponseRedirect('/project_categories/')
            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/project_categories/')
        else:
            locations = Location.objects.all().order_by('-id')
            return render(incoming, 'new/project_categories.html', {'locations': locations})
    else:
        return HttpResponseRedirect('/')


def delete_location(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            code = incoming.GET['code']
            Location.objects.get(code__contains=code).delete()
            messages.success(incoming, 'Location Deleted Successfully')
            return HttpResponseRedirect('/project_categories/')
        except Exception as p:
            print(str(p))
            messages.error(incoming, 'Something is wrong contact system admin')
            return HttpResponseRedirect('/project_categories/')
    else:
        return HttpResponseRedirect('/')


