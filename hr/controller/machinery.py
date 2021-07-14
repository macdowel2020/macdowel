import random
import string
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from hr.models import Staff, Project, AuditTrail, Income, Expenditure, Inventory


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
                return render(request, 'mac/lists/machinery.html', {'projects': projects})
            except Exception as p:
                # print('here')
                # projects = Project.objects.all()
                # return render(request, 'mac/staff_projects.html', {'projects': projects})
                return HttpResponseRedirect('/')

    else:
        messages.error(request, 'You are not allowed to perform this action')
        return HttpResponseRedirect('/')



# def machinary_detail(request):
#     if request.user.is_authenticated:
#         try:
#             total = 0
#             pending_total = 0
#             approved_total = 0
#             rejected_total = 0
#
#             code = request.GET["code"]
#             # get loan details
#             project = Project.objects.get(code=code)
#             staff = Staff.objects.filter(project__code__contains=project.code)
#             userdetail = project.code
#             incomes = Income.objects.filter(project__code__contains=code).order_by('-id')
#             pending_expenditures = Expenditure.objects.filter(project__code__contains=code,
#                                                               status__contains='Pending').order_by('-id')
#             approved_expenditures = Expenditure.objects.filter(project__code__contains=code,
#                                                                status__contains='Approved').order_by('-id')
#             rejected_expenditures = Expenditure.objects.filter(project__code__contains=code,
#                                                                status__contains='Rejected').order_by('-id')
#             inventory = Inventory.objects.filter(project__code__contains=code).order_by('-id')
#
#             # calculate the income total amount
#             for d in incomes:
#                 total += int(d.amount)
#
#             # calculate the pending total amount
#             for d in pending_expenditures:
#                 pending_total += int(d.amount)
#
#             # calculate the approved total amount
#             for d in approved_expenditures:
#                 approved_total += int(d.amount)
#
#             # calculate the rejected total amount
#             for d in rejected_expenditures:
#                 rejected_total += int(d.amount)
#
#             if total > approved_total:
#                 profit = total - approved_total
#             else:
#                 profit = 0
#
#             if total > approved_total:
#                 loss = 0
#             else:
#                 loss = total - approved_total
#             return render(request, 'mac/details/machinary_details.html', {'project': project, 'incomes': incomes,
#                                                                     'total': total,
#                                                                     'pending_expenditures': pending_expenditures,
#                                                                     'pending_total': pending_total,
#                                                                     'approved_expenditures': approved_expenditures,
#                                                                     'approved_total': approved_total,
#                                                                     'rejected_expenditures': rejected_expenditures,
#                                                                     'rejected_total': rejected_total, 'loss': loss,
#                                                                     'profit': profit,
#                                                                     'staff': staff,
#                                                                     'inventory': inventory
#                                                                     })
#         except Exception as p:
#             print(str(p))
#             return HttpResponseRedirect('/staff_projects/')
#     else:
#         messages.error(request, 'Login to Proceed')
#         return HttpResponseRedirect('/')
