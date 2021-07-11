import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Staff, Project, AuditTrail


def machines(request):
    if request.user.is_authenticated:
        staff = Staff.objects.get(user=request.user)
        if request.method == "POST":
            try:
                ds = []
                prox = Project.objects.all()
                for i in prox:
                    ds.append(i.name)

                pro_name = request.POST["name"]
                email = request.POST["email"]
                contact = request.POST["contact"]
                address = request.POST["address"]
                category = request.POST["category"]
                if pro_name not in ds and pro_name != 'Select Option':
                    Project.objects.create(
                        code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                        name=pro_name,
                        email=email,
                        contact=contact,
                        address=address
                    )
                    # record action
                    AuditTrail.objects.create(user=request.user, project=staff.project,
                                              action='Created new Project')
                    messages.success(request, 'Project added successfully')
                    return HttpResponseRedirect('/machines/')
                else:
                    print('Project already exists')
                    messages.error(request, 'Project Already exists')
                    return HttpResponseRedirect('/machines/')

            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/machines/')
        else:
            try:
                projects = Project.objects.all().filter(category='Machinery')
                print('worked')
                return render(request, 'mac/machinery.html', {'projects': projects})
            except Exception as p:
                print('here')
                projects = Project.objects.all()
                return render(request, 'mac/staff_projects.html', {'projects': projects})

    else:
        messages.error(request, 'You are not allowed to perform this action')
        return HttpResponseRedirect('/')