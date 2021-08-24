from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from hr.models import AllProject, Income, Asset


def dashboard(incoming):
    if incoming.user.is_authenticated:
        farm_count = AllProject.objects.all().filter(category__contains='Farm').count()
        machine_count = AllProject.objects.all().filter(category__contains='Machinery').count()
        land_count = AllProject.objects.all().filter(category__contains='Land').count()
        apartment_count = AllProject.objects.all().filter(category__contains='Apartment').count()
        rental_count = AllProject.objects.all().filter(category__contains='Rental').count()

        # Calculate Income
        all_income = 0
        all_land = 0
        all_machinery = 0
        all_apartments = 0
        all_rental = 0

        assets_count = 0

        farm_earned = Income.objects.filter(category='Farm Produce')
        credit_income = Income.objects.filter(project__category__contains='Credit/ Loans')
        insurance_income = Income.objects.filter(project__category__contains='Insurance')
        machine_income = Income.objects.filter(project__category__contains='Machine Income')
        other_income = Income.objects.filter(project__category__contains='Other')

        all_assets = Asset.objects.all()
        for k in all_assets:
            assets_count += int(float(k.cost))

        for i in farm_earned:
            all_income += int(i.amount)

        for i in credit_income:
            all_land += int(i.amount)

        for i in insurance_income:
            all_machinery += int(i.amount)

        for i in machine_income:
            all_apartments += int(i.amount)

        for i in other_income:
            all_rental += int(i.amount)

        return render(incoming, 'dashboard.html', {'farm_count': farm_count, 'machine_count': machine_count,
                                                   'land_count': land_count, 'apartment_count': apartment_count,
                                                   'rental_count': rental_count, 'all_income': all_income,
                                                   'all_land': all_land, 'all_machinery': all_machinery,
                                                   'all_apartments': all_apartments, 'all_rental': all_rental,
                                                   'assets_count': assets_count
                                                   })
    else:
        return HttpResponseRedirect('/login/')


def farms(incoming):
    if incoming.user.is_authenticated:
        try:
            the_farms = AllProject.objects.all().filter(category__contains='Farm').order_by('-id')
            return render(incoming, 'farms.html', {'the_farms': the_farms})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/farms/')
    else:
        messages.error(incoming, 'Login to proceed')
        return HttpResponseRedirect('/')


def lands(incoming):
    if incoming.user.is_authenticated:
        try:
            lands = AllProject.objects.all().filter(category__contains='Land').order_by('-id')
            return render(incoming, 'lands.html', {'lands': lands})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/farms/')
    else:
        messages.error(incoming, 'Login to proceed')
        return HttpResponseRedirect('/')


def delete_land(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            code = incoming.GET['code']
            AllProject.objects.get(code__contains=code).delete()
            messages.success(incoming, 'Project has been Deleted successfully!')
            return HttpResponseRedirect('/lands/')

        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/all_projects/')
    else:
        messages.error(incoming, 'You are not permitted to perform this action')
        return HttpResponseRedirect('/')


def only_machines(incoming):
    if incoming.user.is_authenticated:
        try:
            only_machinesx = AllProject.objects.all().filter(category__contains='Machinery').order_by('-id')
            return render(incoming, 'only_machines.html', {'only_machines': only_machinesx})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/only_machines/')
    else:
        messages.error(incoming, 'Login to proceed')
        return HttpResponseRedirect('/')


def delete_machine(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            code = incoming.GET['code']
            AllProject.objects.get(code__contains=code).delete()
            messages.success(incoming, 'Project has been Deleted successfully!')
            return HttpResponseRedirect('/only_machines/')

        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/only_machines/')
    else:
        messages.error(incoming, 'You are not permitted to perform this action')
        return HttpResponseRedirect('/')


def only_apartments(incoming):
    if incoming.user.is_authenticated:
        try:
            only_apartmentsx = AllProject.objects.all().filter(category__contains='Apartment').order_by('-id')
            return render(incoming, 'only_apartments.html', {'only_apartments': only_apartmentsx})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/only_apartments/')
    else:
        messages.error(incoming, 'Login to proceed')
        return HttpResponseRedirect('/')


def delete_apartment(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            code = incoming.GET['code']
            AllProject.objects.get(code__contains=code).delete()
            messages.success(incoming, 'Project has been Deleted successfully!')
            return HttpResponseRedirect('/only_apartments/')

        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/only_apartments/')
    else:
        messages.error(incoming, 'You are not permitted to perform this action')
        return HttpResponseRedirect('/')


def only_rentals(incoming):
    if incoming.user.is_authenticated:
        try:
            only_rentalsx = AllProject.objects.all().filter(category__contains='Rental').order_by('-id')
            return render(incoming, 'only_rentals.html', {'only_rentals': only_rentalsx})
        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/only_rentals/')
    else:
        messages.error(incoming, 'Login to proceed')
        return HttpResponseRedirect('/')


def delete_rental(incoming):
    if incoming.user.is_authenticated and incoming.user.is_superuser:
        try:
            code = incoming.GET['code']
            AllProject.objects.get(code__contains=code).delete()
            messages.success(incoming, 'Project has been Deleted successfully!')
            return HttpResponseRedirect('/only_rentals/')

        except Exception as p:
            print(str(p))
            return HttpResponseRedirect('/only_rentals/')
    else:
        messages.error(incoming, 'You are not permitted to perform this action')
        return HttpResponseRedirect('/')
