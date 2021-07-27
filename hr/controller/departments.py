import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import Department, AuditTrail, Staff, Role


def dept(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            try:
                # staff = Staff.objects.get(user=request.user)
                dept_name = request.POST["name"]
                Department.objects.create(
                    code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                    name=dept_name
                )
                # record action
                # AuditTrail.objects.create(user=request.user, project=staff.project,
                #                           action='Created new Department')
                messages.success(request, 'Department added successfully')
                return HttpResponseRedirect('/departments/')

            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/departments/')
        else:
            departments = Department.objects.all().order_by('-id')
            return render(request, 'new/departments.html', {'departments': departments})
    else:
        messages.error(request, 'You are not allowed to perform this action')
        return HttpResponseRedirect('/')


def role(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            try:
                # staff = Staff.objects.get(user=request.user)
                ds = []
                rolesx = Role.objects.all()
                for i in rolesx:
                    ds.append(i.name)

                dept_role = request.POST["name"]
                if dept_role not in ds and dept_role != 'Select Option':
                    Role.objects.create(
                        code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                        name=dept_role
                    )
                    # # record action
                    # AuditTrail.objects.create(user=request.user, project=staff.project,
                    #                           action='Created new Role')
                    messages.success(request, 'Access Level added successfully')
                    return HttpResponseRedirect('/roles/')
                else:
                    print('Role already exists')
                    messages.error(request, 'Role Already exists')
                    return HttpResponseRedirect('/roles/')

            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/roles/')
        else:
            roles = Role.objects.all().order_by('-id')
            return render(request, 'new/role.html', {'roles': roles})
    else:
        messages.error(request, 'You are not allowed to perform this action')
        return HttpResponseRedirect('/')


def delete_role(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        name = incoming.GET['name']
        Role.objects.get(name__contains=name).delete()
        return HttpResponseRedirect('/roles/')
    else:
        return HttpResponseRedirect('/')


def delete_department(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        name = incoming.GET['name']
        Department.objects.get(name__contains=name).delete()
        return HttpResponseRedirect('/departments/')
    else:
        return HttpResponseRedirect('/')
