import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from hr.models import Staff, Project, AuditTrail, Income, Expenditure, Inventory

userdetail = ''


def farms(request):
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
                    return HttpResponseRedirect('/farms/')
                else:
                    print('Project already exists')
                    messages.error(request, 'Project Already exists')
                    return HttpResponseRedirect('/farms/')

            except Exception as p:
                print(str(p))
                return HttpResponseRedirect('/farms/')
        else:
            try:
                projects = Project.objects.all().filter(category='Farm')
                print('worked')
                return render(request, 'mac/lists/projects.html', {'projects': projects})
            except Exception as p:
                print('here')
                projects = Project.objects.all()
                return render(request, 'mac/staff_projects.html', {'projects': projects})

    else:
        messages.error(request, 'You are not allowed to perform this action')
        return HttpResponseRedirect('/')


def p_detail(request):
    if request.user.is_authenticated:
        try:
            total = 0
            pending_total = 0
            approved_total = 0
            rejected_total = 0

            code = request.GET["code"]
            # get loan details
            project = Project.objects.get(code=code)
            staff = Staff.objects.filter(project__code__contains=project.code)
            userdetail = project.code
            incomes = Income.objects.filter(project__code__contains=code).order_by('-id')
            pending_expenditures = Expenditure.objects.filter(project__code__contains=code,
                                                              status__contains='Pending').order_by('-id')
            approved_expenditures = Expenditure.objects.filter(project__code__contains=code,
                                                               status__contains='Approved').order_by('-id')
            rejected_expenditures = Expenditure.objects.filter(project__code__contains=code,
                                                               status__contains='Rejected').order_by('-id')
            inventory = Inventory.objects.filter(project__code__contains=code).order_by('-id')

            # calculate the income total amount
            for d in incomes:
                total += int(d.amount)

            # calculate the pending total amount
            for d in pending_expenditures:
                pending_total += int(d.amount)

            # calculate the approved total amount
            for d in approved_expenditures:
                approved_total += int(d.amount)

            # calculate the rejected total amount
            for d in rejected_expenditures:
                rejected_total += int(d.amount)

            if total > approved_total:
                profit = total - approved_total
            else:
                profit = 0

            if total > approved_total:
                loss = 0
            else:
                loss = total - approved_total
            return render(request, 'mac/details/p_detail.html', {'project': project, 'incomes': incomes,
                                                                    'total': total,
                                                                    'pending_expenditures': pending_expenditures,
                                                                    'pending_total': pending_total,
                                                                    'approved_expenditures': approved_expenditures,
                                                                    'approved_total': approved_total,
                                                                    'rejected_expenditures': rejected_expenditures,
                                                                    'rejected_total': rejected_total, 'loss': loss,
                                                                    'profit': profit,
                                                                    'staff': staff,
                                                                    'inventory': inventory
                                                                    })
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/staff_projects/')
    else:
        messages.error(request, 'Login to Proceed')
        return HttpResponseRedirect('/')


def income(request):
    if request.user.is_authenticated:
        try:
            # Get the Staff
            user_staff = request.user.email
            user = Staff.objects.get(user__email__contains=user_staff)
            # Get the project
            code = request.GET['code']
            project = Project.objects.get(code=code)
            print('PROJECT CODE', project.code)

            # Add the income

            amount = request.POST["amount"]
            item = request.POST["item"]
            reason = request.POST["reason"]
            description = request.POST["description"]

            Income.objects.create(
                code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                staff=user,
                project=project,
                amount=amount,
                item=item,
                status='received',
                reason=reason,
                description=description
            )
            messages.success(request, 'You have successfully added an Income')
            return HttpResponseRedirect('/farm_detail/?code=%s'%project.code)
        except Exception as p:
            print(str(p))
            messages.error(request, 'An Error Occured')
    else:
        messages.error(request, 'Login to Proceed')
        return HttpResponseRedirect('/')


def request_expenditure(request):
    if request.user.is_authenticated:
        try:
            # Get the Staff
            user_staff = request.user.email
            user = Staff.objects.get(user__email__contains=user_staff)
            # Get the project
            code = request.GET['code']
            project = Project.objects.get(code=code)

            # Add the income
            amount = request.POST["amount"]
            item = request.POST["item"]
            description = request.POST["description"]

            Expenditure.objects.create(
                code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                staff=user,
                project=project,
                amount=amount,
                item=item,
                status='Pending',
                description=description,
                is_approved=False,
                approved_by=request.user.username
            )
            messages.success(request, 'You have successfully added your request, please wait for approval from MD')
            return HttpResponseRedirect('/farm_detail/?code=%s' % project.code)
        except Exception as p:
            print(str(p))
            messages.error(request, 'An Error Occured')
            return HttpResponseRedirect('/')

    else:
        messages.error(request, 'Login to Proceed')
        return HttpResponseRedirect('/')


def approve_request(request):
    try:
        code = request.GET["code"]
        xp = Expenditure.objects.get(code=code)

        project = Project.objects.get(code=xp.project.code)
        Expenditure.objects.filter(code=code).update(status='Approved')
        messages.success(request, 'You have successfully Approved an Expenditure Request ')
        return HttpResponseRedirect('/farm_detail/?code=%s' % project.code)
    except Exception as p:
        print(str(p))
        messages.error(request, 'An Error Occurred')
        return HttpResponseRedirect('/')


def reject_request(request):
    if request.method == 'POST':
        try:
            code = request.POST["code"]
            reason = request.POST["reason"]
            xp = Expenditure.objects.get(code=code)
            project = Project.objects.get(code=xp.project.code)
            Expenditure.objects.filter(code__contains=code).update(status='Rejected', reason=reason)
            messages.success(request, 'Request has been Rejected')
            return HttpResponseRedirect('/farm_detail/?code=%s' % project.code)
        except Exception as p:
            print(str(p))
            messages.error(request, 'An Error Occurred')
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/farm_detail/?code=%s' % userdetail)


def delete_expenditure(request):
    try:
        code = request.GET["code"]
        Expenditure.objects.get(code=code).delete()
        messages.success(request, 'Request has been Deleted')
        return HttpResponseRedirect('/farms/')
    except Exception as p:
        print(str(p))
        messages.error(request, 'An Error Occurred')
        return HttpResponseRedirect('/')


def delete_income(request):
    try:
        code = request.GET["code"]
    except Exception as p:
        print(str(p))
        messages.error(request, 'An Error Occurred')
        return HttpResponseRedirect('/')


def delete_project(request):
    try:
        code = request.GET["code"]
        Project.objects.get(code__contains=code).delete()
        messages.success(request, 'Project has been deleted Successfully')
        return HttpResponseRedirect('/farms/')

    except Exception as p:
        print(str(p))
        messages.error(request, 'An Error Occurred')
        return HttpResponseRedirect('/')


def update_project_photo(incoming):
    if incoming.user.is_authenticated:
        if incoming.method == 'POST' and incoming.FILES['image']:
            code = incoming.GET["code"]

            image = incoming.FILES['image']
            print(image.name)
            print(image.size)
            xp = Project.objects.get(code__contains=code)

            Project.objects.filter(code__contains=code).update(
                image=image
            )
            fs = FileSystemStorage()
            fs.save(image.name, image)
            messages.success(incoming, 'Project Photo has been Updated Successfully')
            return HttpResponseRedirect('/farm_detail/?code=%s' % xp.code)
        else:
            return HttpResponseRedirect('/farms/')
    else:
        messages.error(incoming, 'Login to proceed!')
        return HttpResponseRedirect('/')


def inventory(request):
    if request.user.is_authenticated:
        try:
            # Get the Staff
            user_staff = request.user.email
            user = Staff.objects.get(user__email__contains=user_staff)
            # Get the project
            code = request.GET['code']
            project = Project.objects.get(code=code)

            # Add the income


            item = request.POST["item"]
            qty = request.POST["qty"]
            unit_price = request.POST["unit_price"]
            description = request.POST["description"]
            date = request.POST["date"]
            reference_copy = request.FILES['reference_copy']
            print(reference_copy.name)
            print(reference_copy.size)


            total_price = float(qty) * float(unit_price)

            Inventory.objects.create(
                code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                staff=user,
                project=project,
                item=item,
                qty = qty,
                unit_price = unit_price,
                total_price = total_price,
                status = 'Completed',
                description = description,
                date=date,
                reference_copy=reference_copy
            )
            fs = FileSystemStorage()
            fs.save(reference_copy.name, reference_copy)
            messages.success(request, 'You have successfully added an Inventory Item')
            return HttpResponseRedirect('/farm_detail/?code=%s' %project.code)
        except Exception as p:
            print(str(p))
            messages.error(request, 'An Error Occured')
    else:
        messages.error(request, 'Login to Proceed')
        return HttpResponseRedirect('/')


def delete_inventory(request):
    try:
        code = request.GET["code"]
        iv =  Inventory.objects.get(code=code)
        Inventory.objects.get(code=code).delete()
        messages.success(request, 'Item has been Deleted')
        return HttpResponseRedirect('/farm_detail/?code=%s' % iv.project.code)
    except Exception as p:
        print(str(p))
        messages.error(request, 'An Error Occurred')
        return HttpResponseRedirect('/')



